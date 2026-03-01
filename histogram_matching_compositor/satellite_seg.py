#!/usr/bin/env python3
"""
Satellite Image Color-Based Region Segmentation

Segments satellite images into:
- Vegetation (Green)
- Water
- Cloud
- Urban

Author: Berk
"""

import cv2
import numpy as np
import argparse
import os




def create_green_mask(hsv):
    """Detect vegetation areas."""
    mask = cv2.inRange(
        hsv,
        np.array([35, 80, 40]),
        np.array([85, 255, 255])
    )
    return mask


def create_water_mask(hsv):
    """Detect water areas."""
    mask = cv2.inRange(
        hsv,
        np.array([75, 20, 20]),
        np.array([140, 255, 255])
    )
    return mask


def create_cloud_mask(hsv):
    """Detect cloud areas."""
    mask = cv2.inRange(
        hsv,
        np.array([0, 0, 200]),
        np.array([180, 60, 255])
    )
    return mask




def calculate_area_ratio(mask, total_pixels):
    return np.sum(mask > 0) / total_pixels * 100




def create_colored_output(image, green_mask, water_mask, cloud_mask):
    result = np.zeros_like(image)

  
    green_mask = cv2.bitwise_and(green_mask, cv2.bitwise_not(water_mask))

    urban_mask = cv2.bitwise_not(
        cv2.bitwise_or(
            cv2.bitwise_or(green_mask, water_mask),
            cloud_mask
        )
    )

    result[green_mask > 0] = [0, 255, 0]      # Green
    result[water_mask > 0] = [0, 0, 255]      # Blue
    result[cloud_mask > 0] = [255, 255, 255]  # White
    result[urban_mask > 0] = [139, 69, 19]    # Brown

    return result, urban_mask



def process_image(input_path, output_path=None, show=False):

    image = cv2.imread(input_path)

    if image is None:
        raise FileNotFoundError("Image could not be loaded. Check file path.")

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    green_mask = create_green_mask(hsv)
    water_mask = create_water_mask(hsv)
    cloud_mask = create_cloud_mask(hsv)

    colored_result, urban_mask = create_colored_output(
        image, green_mask, water_mask, cloud_mask
    )

    total_pixels = image.shape[0] * image.shape[1]

    print("\n========== AREA RATIOS ==========")
    print(f"Green Area  : %{calculate_area_ratio(green_mask, total_pixels):.2f}")
    print(f"Water Area  : %{calculate_area_ratio(water_mask, total_pixels):.2f}")
    print(f"Cloud Area  : %{calculate_area_ratio(cloud_mask, total_pixels):.2f}")
    print(f"Urban Area  : %{calculate_area_ratio(urban_mask, total_pixels):.2f}")

    if output_path:
        output_bgr = cv2.cvtColor(colored_result, cv2.COLOR_RGB2BGR)
        cv2.imwrite(output_path, output_bgr)
        print(f"\nSegmented image saved to: {output_path}")

    if show:
        import matplotlib.pyplot as plt

        plt.figure(figsize=(14, 7))

        plt.subplot(1, 2, 1)
        plt.title("Original Image")
        plt.imshow(image)
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.title("Segmented Result")
        plt.imshow(colored_result)
        plt.axis("off")

        plt.tight_layout()
        plt.show()




if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Satellite Image Region Segmentation (HSV-based)"
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input image"
    )

    parser.add_argument(
        "--output",
        default=None,
        help="Path to save segmented image"
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Display result"
    )

    args = parser.parse_args()

    process_image(
        input_path=args.input,
        output_path=args.output,
        show=args.show
    )