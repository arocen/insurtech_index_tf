import testComputeIndex
import visualize



def testDrawCurves():
    indices = testComputeIndex.testGetIndex()
    plot = visualize.drawCurves(indices)
    return

testDrawCurves()