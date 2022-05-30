# ML models
- To run the trained or pre-trained models, Magenta must be installed. The steps can be found here: [Magenta](http://https://github.com/magenta/magenta/blob/main/README.md "Magenta")

Note: The Magenta project is no longer being maintained in this form, and errors may occur during install which are difficult to fix.

## Pre-trained
- basic_rnn.mag: a pre-trained Melody RNN model from Magenta.
		Run using:  
		& BUNDLE_PATH=basic_rnn.mag CONFIG='basic_rnn'  
		& melody_rnn_generate --config=${CONFIG} --bundle_file=${BUNDLE_PATH} --output_dir=/tmp/melody_rnn/generated --num_outputs=10 --num_steps=128 --primer_melody="[60]"


## Trained on new data
- (to be added)
