#!/bin/bash
echo "Installing Real-ESRGAN..."
git clone https://github.com/xinntao/Real-ESRGAN.git
cd Real-ESRGAN
pip install -r requirements.txt
python setup.py develop
echo "Real-ESRGAN installation complete!"
