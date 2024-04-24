from PIL import ImageEnhance
import os
import random
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Dataset
from torch.optim.lr_scheduler import StepLR
from torch.utils.tensorboard import SummaryWriter
from PIL import Image
import torch.nn.functional as F
import cv2
import numpy as np


if __name__ == '__main__':
    from dataset import HazeDataset


    class DehazeNet(nn.Module):
        def __init__(self):
            super(DehazeNet, self).__init__()
            self.conv1 = nn.Conv2d(in_channels=3, out_channels=3,
                                kernel_size=1, stride=1, padding=0)
            self.conv2 = nn.Conv2d(in_channels=3, out_channels=3,
                                kernel_size=3, stride=1, padding=1)
            self.conv3 = nn.Conv2d(in_channels=6, out_channels=3,
                                kernel_size=5, stride=1, padding=2)
            self.conv4 = nn.Conv2d(in_channels=6, out_channels=3,
                                kernel_size=7, stride=1, padding=3)
            self.conv5 = nn.Conv2d(
                in_channels=12, out_channels=3, kernel_size=3, stride=1, padding=1)

            # Additional refinement layers
            self.refine_conv1 = nn.Conv2d(
                in_channels=3, out_channels=3, kernel_size=3, stride=1, padding=1)
            self.refine_conv2 = nn.Conv2d(
                in_channels=3, out_channels=3, kernel_size=3, stride=1, padding=1)

            self.b = 1

        def forward(self, x):
            x1 = F.relu(self.conv1(x))
            x2 = F.relu(self.conv2(x1))
            cat1 = torch.cat((x1, x2), 1)
            x3 = F.relu(self.conv3(cat1))
            cat2 = torch.cat((x2, x3), 1)
            x4 = F.relu(self.conv4(cat2))
            cat3 = torch.cat((x1, x2, x3, x4), 1)
            k = F.relu(self.conv5(cat3))

            # Refinement layers
            x5 = F.relu(self.refine_conv1(k))
            x6 = F.relu(self.refine_conv2(x5))

            if x6.size() != x.size():
                raise Exception("Output and input image are different sizes!")

            output = x6 * x - x6 + self.b
            return F.relu(output)

    # Set your hyperparameters
    batch_size = 32
    learning_rate = 1e-4
    num_epochs = 500

    # Initialize your model, loss, and optimizer
    device = torch.device('cuda')
    model = DehazeNet().to(device)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    scheduler = StepLR(optimizer, step_size=10, gamma=0.1)

    # Create data loaders for training and validation
    transform = transforms.Compose([
        transforms.Resize([480, 640]),
        transforms.ToTensor()
    ])

    train_dataset = HazeDataset("D:\Dataset\Revside Dataset\Train", transform)
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)

    # Set up TensorBoard
    writer = SummaryWriter()

    # Training loop
    for epoch in range(num_epochs):
        model.train()
        for step, (ground_truth_img, hazy_img) in enumerate(train_loader):
            ground_truth_img, hazy_img = ground_truth_img.to(
                device), hazy_img.to(device)

            # Forward pass
            dehaze_img = model(hazy_img)
            loss = criterion(dehaze_img, ground_truth_img)

            # Backpropagation and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if step % 50 == 0:
                print(
                    f'Epoch [{epoch + 1}/{num_epochs}] Step [{step}/{len(train_loader)}] Loss: {loss.item()}')
                print(f'lr = {learning_rate}')

                # Log the loss to TensorBoard
                writer.add_scalar('Loss/train', loss.item(),
                                  epoch * len(train_loader) + step)

                # Log hazy images, gt, and model outputs as images to TensorBoard
                if step % 500 == 0:
                    # Create a grid of images
                    grid_images = torchvision.utils.make_grid(
                        torch.cat([hazy_img, ground_truth_img, dehaze_img], dim=0), nrow=batch_size
                    )
                    writer.add_image(
                        'Images/hazy_gt_dehaze', grid_images, epoch * len(train_loader) + step)

    # Update the learning rate
    scheduler.step()

    # Close the TensorBoard writer
    writer.close()

    # Save the trained model
    torch.save(model.state_dict(), 'ModelsFinished\DehazeNetDLHaste_Model.pth')

# To use the Model


model = DehazeNet()
model.load_state_dict(torch.load('ModelsFinished\DehazeNet_Model.pth'))
model.eval()  # Set the model to evaluation mode


def dehaze_image(input_image_path, output_image_path):
    # Load and preprocess the input image
    transform = transforms.Compose([
        transforms.Resize([480, 640]),
        transforms.ToTensor()
    ])
    input_image = Image.open(input_image_path)
    input_image = transform(input_image).unsqueeze(0)  # Add batch dimension

    # Perform dehazing
    with torch.no_grad():
        dehazed_image = model(input_image)

    # Convert the dehazed image to a NumPy array
    dehazed_image = dehazed_image.squeeze(0).cpu().numpy()
    dehazed_image = np.clip(dehazed_image, 0, 1)  # Clip values to [0, 1]
    dehazed_image = (dehazed_image * 255).astype(np.uint8)  # Scale to [0, 255]
    dehazed_image = np.transpose(dehazed_image, (1, 2, 0))  # Reshape to HWC

    # Convert the NumPy array back to a PIL image
    dehazed_image = Image.fromarray(dehazed_image)

    # Adjust sharpness, brightness, and contrast
    enhancer = ImageEnhance.Sharpness(dehazed_image)
    # Increase sharpness (adjust as needed)
    dehazed_image = enhancer.enhance(2.0)

    enhancer = ImageEnhance.Brightness(dehazed_image)
    # Lower brightness (adjust as needed)
    dehazed_image = enhancer.enhance(0.8)

    enhancer = ImageEnhance.Contrast(dehazed_image)
    # Increase contrast (adjust as needed)
    dehazed_image = enhancer.enhance(1.2)

    # Save the adjusted image
    dehazed_image.save(output_image_path)


# # Example usage:
# input_image_path = r"C:\Users\Noct\Downloads\screenshot.jpg"
# output_image_path = 'Outputs\DehazedImage.jpg'
# dehaze_image(input_image_path, output_image_path)
