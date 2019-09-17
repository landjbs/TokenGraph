import keras


def build_model(Language):
    """ Returns structure of model for word vector optimization """
    initial_score_vec = keras.layers.Input(shape=(None, Language.vocabSize),
                                            name='initial_score_vec')
    dense_1 =
