from PIL import Image
import os
import sys
#最近碰到了一些图片相关的东西，将已有的图片填充为给定size的图片
#只能说Python果然强大，上代码
#http://effbot.org/imagingbook/image.html
if __name__ == '__main__':
    pic_dic = dict()
    rootdir = '/Users/xuyikai/Downloads/all_logo/logo/'
    #加载图片
    list = os.listdir(rootdir) 
    sum = len(list) - 1
    #不符合尺寸的图，太小了，填充效果太差
    unable = 0
    outdir = '/Users/xuyikai/Downloads/work/img/logo/'
    for i in range(0, len(list)):
        #获取图片路径
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            try:
                im = Image.open(path)
                #处理gif,jpeg图，将其转换为rgb图片，png图不要加此句，png图本身是rgba图片
                if not 'png' in list[i]:
                    im = im.convert('RGB')
                (x, y) = im.size
                #像素低于 150 * 150，统计结果并跳过
                if x < 150 and y < 150:
                    unable += 1
                    continue
                #获取图片格式
                #im_type = im.format
                #加载图片
                img_array=im.load()
                #print img_array[0,0]
                #可以直接获取图片像素点
                #(r, g, b) = img_array[0,0]
                #创建一张新图片，参数分别是：格式，大小，color
                #这里我取的是待扩充图的左上角第一个像素的rgb
                (x, y) = im.size
                z = max(x, y)
                im_new = Image.new('RGBA', (z, z), img_array[0,0])
                #print im_new.format
                #计算旧图片在新图片中放置的位置，其实就是新图片的中间
                pos_x = (z - x) / 2 
                pos_y = (z - y) / 2 
                #旧图粘贴进新图片
                im_new.paste(im, (pos_x, pos_y))
                #resize函数直接拉伸图片，达不到填充的效果，压缩图片的时候可以尝试
                #im_new = im.resize((300, 300), Image.ANTIALIAS)
                im_new.save(outdir + str(list[i]) + '.jpg')
                #统计图片尺寸分布的
                pic_dic.setdefault(str(x) + ',' + str(y), 0)
                pic_dic[str(x) + ',' + str(y)] += 1   
            except:
                s = sys.exc_info()
                print "Error '%s' happened on line %d" % (s[1],s[2].tb_lineno)
            count += 1
    print str(unable) + '\t' + str(sum) 
    #with open('/Users/xuyikai/Downloads/work/pic_size.txt', 'w') as f:
    #    for k, v in pic_dic.iteritems():
      #      f.write(k + '\t' + str(v) + '\n')
        
                
                
                
        
