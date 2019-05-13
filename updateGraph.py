#
#
# def graphBar(xData, y, xAxis, title=None, graphToUpdate=None):
#     if graphToUpdate is None:
#         graphToUpdate = Graph.Graph()
#         graphToUpdate.addGlyph("barres", "VBar", option2="#3AC0C3")
#     graphToUpdate.setXAxis(xAxis)
#     graphToUpdate.setTitle(title)
#     graphToUpdate.changeGlyph("barres", xData, y)
#     graphToUpdate.update()
#     return graphToUpdate
#
# # --------------------------------------------------------------------------------------------------------
#
# def graphQuartile(xData, min, max, q1, q3, title=None, graphToUpdate=None, xAxis=None):
#     if graphToUpdate is None:
#         graphToUpdate = Graph.Graph()
#         graphToUpdate.addGlyph("segments", "VBarQuartile", option1=0.01)
#         graphToUpdate.addGlyph("barres", "VBarQuartile", option1=0.2, option2="#3AC0C3")
#     if xAxis is None:
#         graphToUpdate.setXAxis(xData)
#     else:
#         graphToUpdate.setXAxis(xAxis)
#     graphToUpdate.setTitle(title)
#     graphToUpdate.changeGlyph("segments", x=xData, bottom=min, y=max)
#     graphToUpdate.changeGlyph("barres", x=xData, bottom=q1, y=q3)
#     graphToUpdate.update()
#     return graphToUpdate
#
#


