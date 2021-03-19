from __future__ import print_function
import os
import sys
import math
import time
from PIL import Image, ImageDraw, ImageFilter
from random import randint, randrange, triangular, choice


DEFAULT_WALL_WIDTH = 1280
DEFAULT_WALL_HEIGHT = 800

# DEFAULT_WALL_WIDTH = 1920
# DEFAULT_WALL_HEIGHT = 1080

# DEFAULT_WALL_WIDTH = 515
# DEFAULT_WALL_HEIGHT = 915


#DEFAULT_COLORS = [(255,0,0),(0,255,0),(0,0,255)]
DEFAULT_COLORS = []


class DrawingInImage:
    """
    This class used to draw images utilizing lines, points and polygons
    """

    def __init__(self):

        self.width = DEFAULT_WALL_WIDTH
        self.height = DEFAULT_WALL_HEIGHT
        self.repetition = 10
        self.box_width = 5
        self.box_height = 5
        self.blank_image = Image.new('RGB',
                                     (self.width, self.height),
                                     color=(0, 0, 0))
        self.draw = ImageDraw.Draw(self.blank_image)

        self.drawPolygon(20)

    def __repr__(self): return f"{type(self).__name__}()"

    def random_color(self): return (round(randrange(0, 255)),
                                    round(randrange(0, 255)),
                                    round(randrange(0, 255)))

    def drawLine(self, reps):
        """
        Draws a line with random x and y coordinate
        """
        for _ in range(reps):

            self.x_val = triangular(-5, self.width)
            self.y_val = triangular(-5, self.height)
            self.x2_val = self.x_val + randrange(self.box_width)
            self.y2_val = self.y_val + randrange(self.box_height)
            self.draw.line([self.x_val, self.y_val, self.x2_val, self.y2_val],
                           fill=self.random_color(),
                           width=1
                           )

    def drawPoint(self, reps):
        """
        Draw points at random places utilizing triangular random selection
        """
        for _ in range(reps):
            self.x_val = triangular(-5, self.width)
            self.y_val = triangular(-5, self.height)
            self.x2_val = self.x_val + randrange(self.box_width)
            self.y2_val = self.y_val + randrange(self.box_height)
            self.draw.point([self.x_val, self.y_val, self.x2_val, self.y2_val],
                            fill=self.random_color(),
                            )

    def drawPolygon(self, reps):
        for _ in range(reps):
            self.x_val = triangular(-5, self.width)
            self.y_val = triangular(-5, self.height)
            self.x2_val = self.x_val + randrange(self.box_width)
            self.y2_val = self.y_val + randrange(self.box_height)
            self.draw.polygon(
                [
                    choice([self.x_val*2, -self.x_val]),
                    choice([self.y_val*2, -self.y_val]),
                    choice([self.x2_val//2, -self.x2_val]),
                    choice([self.y2_val//2, -self.y2_val]),
                    choice([-self.y_val*2, self.y_val*2]),
                    choice([-self.x_val*2, self.x_val*2]),
                    choice([-self.y_val//2, self.y_val*2]),
                    choice([-self.x_val//2, self.x_val//2])
                ],
                fill=choice(DEFAULT_COLORS) if len(DEFAULT_COLORS) > 1 else self.random_color())

    def return_im(self):
        return self.blank_image

    def save(self, filename):
        self.blank_image.save(filename)


class Lines(DrawingInImage):
    """
    Filter_imag("input.png")
    """

    def __init__(self, filename):
        self.image = filename
        self.pix = self.image.load()
        self.size = self.image.size

        self.line_len_factor: int = round(self.size[0]*.03)
        self.line_wid: int = 1

        self.blank_image = self.image
        # self.blank_image = Image.new('RGB', (self.size[0], self.size[1]))

        self.draw = ImageDraw.Draw(self.blank_image)

        print("line_len_factor : ", self.line_len_factor)
        print("line_wid : ", self.line_wid)
        print("size : ", self.size)

        list_start_time: float = time.time()

        list(
            map(
                lambda width:
                list(
                    map(lambda height:

                        self.draw.line(
                            [width,
                             height,
                             round(
                                 width + round(sum(self.pix[width, height])/self.line_len_factor) * math.cos(randint(0, 360))),
                             round(
                                 height + round(sum(self.pix[width, height])/self.line_len_factor) * math.sin(randint(0, 360)))],

                            fill=self.pix[width, height],
                            width=self.line_wid
                        ),
                        range(self.size[1])
                        )
                ),
                range(self.size[0])
            )
        )

        print("List Comprehension finished in", str(
            (time.time()-list_start_time)))


class Circles(DrawingInImage):
    """Circles("input.png")"""

    def __init__(self, filename):
        self.filename = filename
        self.image = self.im = self.filename
        self.im = self.image.filter(ImageFilter.GaussianBlur(radius=5))
        self.pix = self.im.load()
        self.size = self.im.size
        self.line_wid: int = 1
        self.circle_radius_factor = 20
        self.division = 5
        self.blank_image = self.image
        # self.blank_image = Image.new(
        # 'RGB', (self.size[0], self.size[1]), color=(0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
        print('circle_radius_factor : ', self.circle_radius_factor)
        print('size : ', self.size)

        self.circle_lining()

    def circle_lining(self):
        list_start_time = time.time()

        list(map(lambda width:
                 list(map(lambda height:
                          self.draw.ellipse(
                              [
                                  round(
                                      width * self.division - round(sum(self.pix[width * self.division, height * self.division])/self.circle_radius_factor) * math.cos(randint(0, 360))),
                                  round(
                                      height * self.division - round(sum(self.pix[width * self.division, height * self.division])/self.circle_radius_factor) * math.cos(randint(0, 360))),
                                  round(
                                      width * self.division+round(sum(self.pix[width * self.division, height * self.division])/self.circle_radius_factor) * math.cos(randint(0, 360))),
                                  round(
                                      height * self.division+round(sum(self.pix[width * self.division, height * self.division])/self.circle_radius_factor) * math.cos(randint(0, 360)))
                              ],
                              outline=self.pix[width * self.division,
                                               height * self.division],
                              fill=self.pix[width * self.division, height * self.division]),
                          range(self.size[1]//self.division))),
                 range(self.size[0]//self.division)))

        print('List Comprehension finished in', time.time()-list_start_time)


current_wd = os.path.dirname(os.path.realpath(sys.argv[0]))
walls_directory = os.path.join(current_wd, "walls")


if __name__ == '__main__':
    wall_num = 0
    for i in range(5):
        # list(map(lambda x: putToScreen.drawLine(), range(500)))

        wall_num += 1
        cool_images = Circles(Lines(DrawingInImage().return_im()).return_im())

        if not os.path.exists(walls_directory):
            os.makedirs(walls_directory)
        filename = os.path.join(walls_directory, f'wall{wall_num}.png')
        print(str(f"{wall_num:05}") + "-"*(10-len(str(wall_num))) +
              f'wall{wall_num}.png\n')

        cool_images.save(filename)

    print(
        f"\nSuccessfully created {wall_num} random wallpapers\n")
