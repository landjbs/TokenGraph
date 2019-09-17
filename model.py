import keras


def build_model(Language):
    """ Returns structure of model for word vector optimization """
    inputs = keras.layers.Input(shape-=(None, Language.vocabSize))
