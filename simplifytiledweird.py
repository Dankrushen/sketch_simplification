import torch
from torchvision import transforms
from torchvision.utils import save_image
from torch.utils.serialization import load_lua

from PIL import Image
import argparse
import math

parser = argparse.ArgumentParser(description='Sketch simplification demo.')
parser.add_argument('--model', type=str, default='model_gan.t7', help='Model to use.')
parser.add_argument('--img',   type=str, default='test.png',     help='Input image file.')
parser.add_argument('--out',   type=str, default='out.png',      help='File to output.')
opt = parser.parse_args()

use_cuda = torch.cuda.device_count() > 0

tile_size = 300

cache  = load_lua( opt.model,long_size=8 )
model  = cache.model
immean = cache.mean
imstd  = cache.std
model.evaluate()

fullimage = Image.open( opt.img ).convert('L')
full_x = fullimage.size[0]
full_y = fullimage.size[1]

imagetiles = []
xtiles = math.ceil(full_x / tile_size)
ytiles = math.ceil(full_y / tile_size)
#print("x: " + str(fullimage.size[0]) + " y: " + str(fullimage.size[1]))
#print("x_tiles: " + str(xtiles) + " y_tiles: " + str(ytiles))

for ytile in range( ytiles ):
   for xtile in range( xtiles ):
      x_coord = xtile * tile_size
      y_coord = ytile * tile_size

      x_length = tile_size
      if xtile >= ( xtiles - 1 ):
         x_length = full_x % tile_size

      y_length = tile_size
      if ytile >= ( ytiles - 1 ):
         y_length = full_y % tile_size

      #print("x: " + str(x_length) + " y: " + str(y_length))

      #print("left: " + str(x_coord) + " upper: " + str(y_length) + " right: " + str(x_coord + x_length) + " lower: " + str(y_coord + y_length))
      
      cropped_img = fullimage.crop( [x_coord, y_coord, ( x_coord + x_length ), ( y_coord + y_length )] )
      cropped_img.load()
      imagetiles.append( cropped_img )

fullimage.close()
del fullimage

out_imagetiles = []
for tile in imagetiles:
   data  = tile
   w, h  = data.size[0], data.size[1]
   pw    = 8-(w%8) if w%8!=0 else 0
   ph    = 8-(h%8) if h%8!=0 else 0
   data  = ((transforms.ToTensor()(data)-immean)/imstd).unsqueeze(0)
   if pw!=0 or ph!=0:
      data = torch.nn.ReplicationPad2d( (0,pw,0,ph) )( data ).data

   if use_cuda:
      pred = model.cuda().forward( data.cuda() ).float()
   else:
      pred = model.forward( data )
   
   out_imagetiles.append( pred[0] )

out_image = Image.new('L', [full_x, full_y])

for ytile in range( ytiles ):
   for xtile in range( xtiles ):
      x_coord = xtile * tile_size
      y_coord = ytile * tile_size
      
      out_image.paste( transforms.ToPILImage()( out_imagetiles[xtile + ytile].cpu() ), [x_coord, y_coord] )

#save_image( pred[0], opt.out )
out_image.save( opt.out )

