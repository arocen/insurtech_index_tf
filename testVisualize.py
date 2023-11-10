import testComputeIndex
import visualize


def testNoweight():
    '''draw curves in the condition that indices are not weighted'''
    indices = testComputeIndex.testGetIndex()
    visualize.drawCurves(indices)
    return

def testDrawCurves():
    '''indices are weighted'''
    indices = testComputeIndex.testDivide()
    visualize.drawCurves(indices)
    return



testDrawCurves()
# testNoweight()