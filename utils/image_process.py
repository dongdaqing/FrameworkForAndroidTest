__author__ = 'dongdaqing'

from PIL import Image

class ImageProcess(object):

    def __init__(self):
        pass

    def make_regalur_image(self, img, size = (256, 256)):
        return img.resize(size).convert('RGB')

    def split_image(self, img, part_size = (64, 64)):
        w, h = img.size
        pw, ph = part_size

        assert w % pw == h % ph == 0

        return [img.crop((i, j, i+pw, j+ph)).copy()\
                for i in xrange(0, w, pw)\
                for j in xrange(0, h, ph)]

    def hist_similar(self, lh, rh):
        assert len(lh) == len(rh)
        return sum(1 - (0 if l == r else float(abs(l - r))/max(l, r)) for l, r in zip(lh, rh))/len(lh)

    def calc_similar(self, li, ri):
    #	return hist_similar(li.histogram(), ri.histogram())
        return sum(self.hist_similar(l.histogram(), r.histogram()) for l, r in zip(self.split_image(li), self.split_image(ri))) / 16.0


    def calc_similar_by_path(self, lf, rf):
        li, ri = self.make_regalur_image(Image.open(lf)), self.make_regalur_image(Image.open(rf))
        return self.calc_similar(li, ri)

if __name__ == '__main__':
    path = r'test/TEST%d/%d.JPG'
    img_obj = ImageProcess()
    for i in xrange(1, 8):
        print 'test_case_%d: %.3f%%'%(i,\
                    img_obj.calc_similar_by_path('doc/image_process/test/TEST%d/%d.JPG'%(i, 1), 'doc/image_process/test/TEST%d/%d.JPG'%(i, 2))*100)