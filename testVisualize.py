import testComputeIndex
import visualize


def testNoweight():
    '''draw curves in the condition that indices are not weighted'''
    indices = testComputeIndex.testGetIndex()
    plot = visualize.drawCurves(indices)
    return

def testDrawCurves():
    '''indices are weighted'''
    indices = testComputeIndex.testDivide()
    plot = visualize.drawCurves(indices)
    return



testDrawCurves()
# testNoweight()