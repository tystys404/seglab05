from PIL import Image

picref_path = "1.png"
picref = Image.open(picref_path)
picrefNew = []
picrefNew.append(picref)
picrefNew[0].save("./1.gif", 'gif', save_all=True, append_images=picrefNew[1:])
