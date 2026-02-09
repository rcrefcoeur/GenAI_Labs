### Why might lower ranks produce noisier outputs?

In LoRA the pre-trained model is frozen, and only a few trainable parameters are fed into the model. Because of the low number of parameters, the model can only approximate the representation of the target image, resulting in noise or artefacts.

### What signs indicate your model is overfitting?

When the model is overfitting, it is less influenced by the prompt, and it would keep repeating what is already in the model, resulting it images all looking the same. 

### How would you adapt these settings for a different style (e.g., photorealistic portraits)?

For photorealistic portraits, instead of remembering the style of drawing, the model will need to memorize facial features. For this is will need a sufficiently large dataset of training images. Images will need to be of higher resolution.