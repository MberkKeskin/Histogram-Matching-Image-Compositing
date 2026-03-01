# Histogram-Matching-Image-Compositing
This project performs histogram matching between two images and enables ROI-based object compositing using classical computer vision techniques.

It aligns color distributions between images and visualizes RGB histograms before and after matching.

Features:
RGB histogram visualization
ROI selection using OpenCV
Histogram matching (color transfer)
Object compositing onto reference image
Automatic result saving
Command-line interface support

Installation:

Clone the repository:

git clone https://github.com/MberkKeskin/Histogram-Matching-Image-Compositing

cd histogram-matching-compositor

pip install opencv-python numpy matplotlib scikit-image

python histogram_matching_compositor.py --imageA imageA_Path --imageB imageB_Path
