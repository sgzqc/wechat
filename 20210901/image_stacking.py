import numpy as np
import scipy.stats as stats
import imageio
import glob
from _utils import panel,histogram


def stackRead(pathname):
    '''
    pathname defined by "glob" pattern.
    i.e.: "directory/sequence_folder/image_*.jpg"
    '''
    SEQ_IMG = glob.glob(pathname)
    n = len(SEQ_IMG)
    print("total num is {}".format(n))
    sample = imageio.imread(SEQ_IMG[0])
    # x and y are the dimensions
    # c is the number of channels
    y, x, c = sample.shape  # (512,512,4)
    # define stack
    stack = np.zeros((n, y, x, c), dtype=sample.dtype)
    # image stacking
    for FILE in SEQ_IMG:
        index = SEQ_IMG.index(FILE)
        image = imageio.imread(FILE)
        stack[index] = image
    return stack


def blendStack(stack, modo='median', axis=0):
    if modo == 'sum':
        blend = np.sum(stack, axis)
    if modo == 'arithmetic mean':
        blend = np.mean(stack, axis)
    if modo == 'geometric mean':
        blend = stats.gmean(stack, axis)
    if modo == 'harmonic mean':
        blend = stats.hmean(stack, axis)
    if modo == 'median':
        blend = np.median(stack, axis)
    if modo == 'minimum':
        blend = np.amin(stack, axis)
    if modo == 'maximum':
        blend = np.amax(stack, axis)
    if modo == 'curtosis':
        blend = stats.kurtosis(stack, axis)
    if modo == 'variance':
        blend = np.var(stack, axis)
    if modo == 'standard deviation':
        blend = np.std(stack, axis)

    return blend.astype(stack.dtype)


if __name__ == "__main__":
    stack = stackRead('./image/sample.*.jpg')
    # print(len(stack))
    panel(stack , (3, 1),
          interval=[0, 255],
          dims=(1200, 400),
          texts=['{:04}'.format(i + 1) for i in range(10)],
          save_text = "./result/stack.jpg"
          )

    median = blendStack(stack)
    sample_blend = np.array([stack[0] , median ])
    panel(sample_blend, (2, 1),
          interval=[0, 1],
          texts=['sample 0001', 'median'],
          save_text= "./result/median.jpg"
          )

    mean_a = blendStack(stack, modo='arithmetic mean')
    mean_g = blendStack(stack, modo='geometric mean')
    mean_h = blendStack(stack, modo='harmonic mean')
    sample_blend = np.array([mean_a, mean_g, mean_h])
    panel(sample_blend, (3, 1),
          dims=(1200, 400),
          interval=[0, 1],
          texts=['arithmetic mean', 'geometric mean', 'harmonic mean'],
          save_text = './result/mean.jpg',
          )

    minimum = blendStack(stack , modo='minimum')
    maximum = blendStack(stack , modo='maximum')
    sample_blend = np.array([minimum, maximum])
    panel(sample_blend, (2, 1),
          interval=[0, 1],
          texts=['minimum', 'maximum'],
          save_text= './result/extremes.jpg'
          )

    curtosis = blendStack(stack,modo='variance')
    sample_blend = np.array([stack[0], curtosis])
    panel(sample_blend, (2, 1),
          interval=[0, 1],
          texts=['sample 0001', 'variance'],
          save_text= './result/variance.jpg'
          )


