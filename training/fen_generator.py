import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # '0' for INFO and WARNING messages, '1' for only WARNING messages, '2' for only ERROR messages, and '3' for no messages.
import tensorflow as tf
tf.get_logger().setLevel('ERROR') # Only show error messages
import numpy as np
from helper_functions import shortenFEN, unflipFEN
import helper_image_loading
import chessboard_finder



def load_graph(frozen_graph_filepath):
    # Load and parse the protobuf file to retrieve the unserialized graph_def.
    with tf.io.gfile.GFile(frozen_graph_filepath, "rb") as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())

    # Import graph def and return.
    with tf.Graph().as_default() as graph:
        # Prefix every op/nodes in the graph.
        tf.import_graph_def(graph_def, name="tcb")
    return graph


class ChessboardPredictor(object):
    """ChessboardPredictor using saved model"""

    def __init__(self, frozen_graph_path='training/model/best.pb'):
        # Restore model using a frozen graph.
        print("\t Loading model '%s'" % frozen_graph_path)
        graph = load_graph(frozen_graph_path)
        self.sess = tf.compat.v1.Session(graph=graph)

        # Connect input/output pipes to model.
        self.x = graph.get_tensor_by_name('tcb/Input:0')
        self.keep_prob = graph.get_tensor_by_name('tcb/KeepProb:0')
        self.prediction = graph.get_tensor_by_name('tcb/prediction:0')
        self.probabilities = graph.get_tensor_by_name('tcb/probabilities:0')
        print("\t Model restored.")

    def getPrediction(self, tiles):
        """Run trained neural network on tiles generated from image"""
        if tiles is None or len(tiles) == 0:
            print("Couldn't parse chessboard")
            return None, 0.0

        # Reshape into Nx1024 rows of input data, format used by neural network
        validation_set = np.swapaxes(np.reshape(tiles, [32 * 32, 64]), 0, 1)

        # Run neural network on data
        guess_prob, guessed = self.sess.run(
            [self.probabilities, self.prediction],
            feed_dict={self.x: validation_set, self.keep_prob: 1.0})

        # Prediction bounds
        a = np.array(list(map(lambda x: x[0][x[1]], zip(guess_prob, guessed))))
        tile_certainties = a.reshape([8, 8])[::-1, :]

        # Convert guess into FEN string
        # guessed is tiles A1-H8 rank-order, so to make a FEN we just need to flip the files from 1-8 to 8-1
        labelIndex2Name = lambda label_index: ' KQRBNPkqrbnp'[label_index]
        pieceNames = list(map(lambda k: '1' if k == 0 else labelIndex2Name(k), guessed))  # exchange ' ' for '1' for FEN
        fen = '/'.join([''.join(pieceNames[i * 8:(i + 1) * 8]) for i in reversed(range(8))])
        return fen, tile_certainties

    def close(self):
        print("Closing session.")
        self.sess.close()


###########################################################
# MAIN CLI

def start_detection(filepath=None, unflip=False, active='w'):
    # Load image from filepath
    # global img

        # Load image from file
    img = helper_image_loading.loadImageFromPath(filepath)

    # Look for chessboard in image, get corners and split chessboard into tiles
    tiles, corners = chessboard_finder.findGrayscaleTilesInImage(img)

    # Exit on failure to find chessboard in image
    if tiles is None:
        raise Exception('Couldn\'t find chessboard in image')

    if filepath:
        print("\n--- Prediction on file %s ---" % filepath)

    # Initialize predictor, takes a while, but only needed once
    predictor = ChessboardPredictor()
    fen, tile_certainties = predictor.getPrediction(tiles)
    predictor.close()
    if unflip:
        fen = unflipFEN(fen)
    short_fen = shortenFEN(fen)
    # Use the worst case certainty as our final uncertainty score
    certainty = tile_certainties.min()

    print('Per-tile certainty:')
    print(tile_certainties)
    print("Certainty range [%g - %g], Avg: %g" % (
        tile_certainties.min(), tile_certainties.max(), tile_certainties.mean()))

    print("---\nPredicted FEN:\n%s %s - - 0 1" % (short_fen, active))
    print("Final Certainty: %.1f%%" % (certainty * 100))
    result = str(short_fen + " " + active + " - - 0 1")
    return result


if __name__ == '__main__':
    start_detection(filepath="./train_data/checker.png")
