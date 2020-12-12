import os
import argparse
from PIL import Image, ImageDraw

PLANET_ORBITS = {
    'sun': 0,
    'mercury': 57.9,
    'venus': 108.2,
    'earth': 149.6,
    'mars': 227.9,
    'jupiter': 778.6,
    'saturn': 1433.5,
    'uranus': 2872.5,
    'neptune': 4495.1,
    'pluto': 5906.4
}
PLANET_NAMES = ['sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']

def main():
    # Parse the program arguments
    parser = argparse.ArgumentParser(prog='planetlabels', description='Generates the labels '+\
        'used in the multi-spectral location tattoo.')
    parser.add_argument('--dimension', nargs=1, default=[100], type=int, required=False,\
        help='The marker dimensions in [heigh width].')
    parser.add_argument('--blocks', nargs=1, default=[9], type=int, required=True,\
        help='The number of blocks to define the ratios in the image.')
    parser.add_argument('--padding', nargs=1, default=[10], type=int, required=False,\
        help='The extra padding between blocks.')
    args = parser.parse_args()

    # Scale the distances to fit the block count
    scalar = (1.0/PLANET_ORBITS[PLANET_NAMES[-1]])*(2**args.blocks[0])
    for key in PLANET_ORBITS.keys():
        PLANET_ORBITS[key] = PLANET_ORBITS[key]*scalar

    # Create the labels
    for key in PLANET_ORBITS.keys():
        # Set up image interaction
        img = Image.new('RGBA', ((args.dimension[0]+args.padding[0])*args.blocks[0],\
            args.dimension[0]+args.padding[0]), (0,0,0,0))
        draw = ImageDraw.Draw(img)

        # Draw each bit
        for i in range(args.blocks[0]):
            def topleft(index):
                return ((index*(args.dimension[0]+args.padding[0]))+(args.padding[0]/2),\
                    args.padding[0]/2)
            def bottomRight(xy):
                return (xy[0]+args.dimension[0], xy[1]+args.dimension[0])
            bit = (int(PLANET_ORBITS[key]) >> i) & 0b1
            if bit == 0: continue

            xy0 = topleft(i)
            xy1 = bottomRight(xy0)
            draw.ellipse((xy0, xy1), fill=(255, 255, 255, 255))
        
        # Save and clean up
        del draw
        img.save(str(key)+'-label.png')

if __name__ == '__main__':
    main()
