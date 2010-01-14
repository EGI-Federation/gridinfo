# This file is part of the GridMap software (see http://gridmap.cern.ch)
# Copyright (c) EDS and CERN 2007, patent pending
#
# Author: Max Boehm, max.boehm@eds.com, max.boehm@cern.ch
#
# History:
# 18.09.2007  mb        first internal version
# 19.10.2007  mb        1st deployed version, showed at EGEE'07 conference
# 25.11.2007  mb        release v01, complete overwork
# 26.02.2009  mb        support for a default size of sites with no size informatiton
#

import math


class TreeMap:

    # initialize internal data attributes:
    # - x, y, width, height
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    # input:
    # - data = [(obj, size)]
    #
    # create internal data attributes:
    # - l = [(size, sum, obj)]
    # - total = sum of sizes
    # - c = width*height/total
    def set_data(self, data):

        # copy data and sort according to size in decreasing order
        sorted_data = list(data)
        sorted_data.sort(lambda x,y: cmp(y[1],x[1]))
        
        # prepare internal list l = [(size, sum, obj)], drop items with size<=0
        s = 0
        self.l = []
        for obj, size in sorted_data:
            if size <= 0:
                print "warning: size=%d, %s ignored!" % (size, obj)
            else:
                s = s + size
                self.l.append((size, s, obj))
        self.total = s

        # c is scaling factor
        if s>0:
            self.c = float(self.width)*self.height/self.total
        else:
            self.c = 0

        return

    # internal function
    # calculate quality if l[i]..l[j] are put into column of height h
    # returns w, q
    def quality(self, i, j, h):
        
        s = self.l[j][1]                # sum[j]
        if i>0:
            s = s - self.l[i-1][1]      # sum[i-1]

        w = float(s)*self.c/h

        hi = self.l[i][0]*self.c/w       # size[i]
        hj = self.l[j][0]*self.c/w       # size[j]

        q = max(hi/w, w/hj)
        return w, q

    # internal function
    # calculate one part l[i]..l[i+cnt-1] to put into column of height h
    # (be greedy until quality no longer improves)
    # returns cnt, w, q
    def part(self, i, h, th):
        cnt = 1
        h = h - th
        w, q = self.quality(i, i, h)
        while i+cnt < len(self.l):
            h = h - th
            wj, qj = self.quality(i, i+cnt, h)
            if qj >= q:
                break
            cnt, w, q = cnt+1, wj, qj
        return cnt, w, q

    # internal function
    # calculate all parts l[i]..l[i+cnt-1], return them in a list
    # th=0 means squarified layout, th>0 means column layout with title height th
    # returns p = [(i, cnt, wp or hp, q, is_vert)]
    def calc_parts(self, th):
        w = self.width
        h = self.height
        # if th>0 then is_vert=True
        p = []      # p = [(i, cnt, wp or hp, q, is_vert)]
        i = 0
        while i < len(self.l):
            if w > h or th > 0:         # vertical strip
                (cnt, wp, q) = self.part(i, h, th)
                p.append((i, cnt, wp, q, True))
                w = w-wp
            else:                       # horizontal strip
                (cnt, hp, q) = self.part(i, w, 0)
                p.append((i, cnt, hp, q, False))
                h = h-hp
            i = i+cnt
                
        # if th=0 then assert(w*h=0)
        assert th!=0 or abs(w*h)<0.00001

        # optional heuristics to improve the last 2 columns of the column layout
        if th > 0 and len(p) >= 2:
            # heuristic a) -> keep two columns, optimize splitting point
            i = p[-2][0]
            j = p[-1][0]
            q = p[-2][3]+p[-1][3]
            while j>i+1:
                j = j-1
                # print "i=%d j=%d h=%d" % (i,j,h)
                (wi, qi) = self.quality(i, j-1, h-(j-i)*th)
                (wj, qj) = self.quality(j, len(self.l)-1, h-(len(self.l)-j)*th)
                if qi+qj >= q:
                    break
                print "heuristic a) applied: [%d..%d] [%d..%d]" % (i, j-1, j, len(self.l)-1)
                p[-2] = (i, j-i, wi, qi, True)
                p[-1] = (j, len(self.l)-j, wj, qj, True)

            # heuristic b) -> merge the last two columns into one column
            (wi, qi) = self.quality(i, len(self.l)-1, h-(len(self.l)-i)*th)
            if qi < q:
                print "heuristic b) applied: [%d..%d]" % (i, len(self.l)-1)
                p[-2] = (i, len(self.l)-i, wi, qi, True)
                del p[-1]
        return p

    # helper to return a rectangle with coordinates rounded to integer
    def rect(self, x, y, w, h):
        if w < 0:
            w = 0
        if h < 0:
            h = 0
        return int(x+0.5), int(y+0.5), int(x+w+0.5)-int(x+0.5), int(y+h+0.5)-int(y+0.5)

    # calculate treemap in "Column Layout" (columns with titles of height th)
    # first column starts at position (self.x+dx1, self.y)
    # insert dx2 space between columns
    # returns rects = [ ((x, y, w, h), size, obj) ]
    def column_layout(self, th, dx1=1, dx2=1):

        p = self.calc_parts(th)         # calculate parts of treemap

        # correction: due to the size needed by the titles, the width needs to be scaled down
        total_w = 0
        for i, cnt, w, q, vert in p:
            total_w = total_w + w
        if total_w>0:
            scale = float(self.width-dx1-(len(p)-1)*dx2)/total_w
        else:
            scale = 1
        
        x = self.x
        y = self.y
        rects = []
        x = x + dx1                     # add left margin
        for i, cnt, w, q, vert in p:    # part l[i]..l[i+cnt-1] with width w
            w = w * scale               # scale down to desired width
            yj = y
            for j in range(i, i+cnt):
                yj = yj+th
                h = self.l[j][0]*self.c*scale/w     # calculate h from the size of item
                r = self.rect(x, yj, w, h)
                if r[2]>0 and r[3]>0:
                    rects.append((r, self.l[j][0], self.l[j][2]))  # size[j], obj[j]
                yj = yj+h
            x = x + w + dx2             # add space between columns

        return rects

    # calculate treemap in "Squarified Layout" (columns and rows)
    # rects w/h are reduced by 1
    # returns rects = [ ((x, y, w, h), size, obj) ]
    def squarified_layout(self):

        p = self.calc_parts(0)          # calculate parts of treemap

        x = self.x
        y = self.y
        rects = []
        for i, cnt, wh, q, vert in p:
            if vert:
                yj = y
                for j in range(i, i+cnt):
                    h = self.l[j][0]*self.c/wh      # calculate h from the size of item
                    rects.append((self.rect(x, yj, wh-1, h-1), self.l[j][0], self.l[j][2])) # size[j], obj[j]
                    yj = yj+h
                x = x+wh
            else:
                xj = x
                for j in range(i, i+cnt):
                    w = self.l[j][0]*self.c/wh
                    rects.append((self.rect(xj, y, w-1, wh-1), self.l[j][0], self.l[j][2])) # size[j], obj[j]
                    xj = xj+w
                y = y+wh
        return rects


# Calculates a GridMap layout
#
# Input:
# - posx, posy, width, height    the bounding box
# - th                           the title height
# - topology                     {regionname: [sitelist]}
# - sitedata                     reference data, contains global metrics of sites, #CPUs
# - sizefunc                     to extract the metric to be used for the size of the rectangles
# - default                      sites with unknown size will be sized: average_size*default/100
#
# topology = {regionname: [sites]}
# Defines a 2 level hierarchy. The union of the sites in this topology is a subset of
# the sites contained in sitedata. Different topologies can exist, e.g. regions, tiers, etc.
#
# sitedata = {sitename: metrics}
# - sitename  is a string
# - metrics   can be any object (a user defined function is used for extracting the size)
#
# sizefunc
# Function to extract the size value from the metrics object in sitedata. This will be used for
# the size of site rectangles in the treemap.
#
# returns out_regions, out_sites
# - out_regions = {regionname: [x, y, w, size]}
# - out_sites   = {sitename: [x, y, w, h, size]}
#
def create_GridMap_layout(posx, posy, width, height, th, topology, sitedata, sizefunc, default=0):

    out_regions = {}
    out_sites = {}

    # 1st level
    # prepare region data: data = [(regionname, size)]
    data = []
    region_default = {}
    for regionname, sitelist in topology.iteritems():
        # list of sites which have size data
        sitelist_filtered = filter(lambda s: sitedata.has_key(s), sitelist)
        # sum of the sizes of these sites
        region_sum = sum(map(lambda s: sizefunc(sitedata[s]), sitelist_filtered))
        # default size for sites of this region which do not have size data
        region_default[regionname] = int(default*region_sum/max(len(sitelist_filtered), 1)/100)
        region_default_count = len(sitelist)-len(sitelist_filtered)
        # setup the data for the region treemap
        data.append((regionname, region_sum+region_default[regionname]*region_default_count))

    tm = TreeMap(posx, posy, width, height)
    tm.set_data(data)

    # Heuristic to adapt internal scaling factor, such that space for titles are better taken into account
    # (this is an optional step but results is a better aspect ratio of rectangles in the column layout)
    if width*height>0:
        space_for_title_estimation = th*math.sqrt(len(data)*width*height)
        tm.c = tm.c * max((width*height-space_for_title_estimation)/(width*height), 0.1)

    rects = tm.column_layout(th)        # [ ((x, y, w, h), regionsize, regionname) ]

    for (x, y, w, h), regionsize, regionname in rects:
        # duplicated regionnames are not allowed
        assert not out_regions.has_key(regionname)

        if regionsize==0 or w==0 or h==0:
            continue
        
        # 2nd level
        # prepare site data: data = [(sitename, size)]
        data = []
        for sitename in topology[regionname]:
            if sitedata.has_key(sitename):
                data.append((sitename, sizefunc(sitedata[sitename])))
            else:
                data.append((sitename, region_default[regionname]))

        tm2 = TreeMap(x, y, w, h)
        tm2.set_data(data)
        rects2 = tm2.squarified_layout() # [ ((x, y, w, h), sitesize, sitename) ]

        # save the output
        # save region title layout [x, y, w, regionsize]
        out_regions[regionname] = [x, y, w, regionsize]

        for (x, y, w, h), sitesize, sitename in rects2:
            # assert not out_sites.has_key(sitename)
            if out_sites.has_key(sitename):
                print "warning: out_sites.has_key(%s), %s will be ignored!" % (sitename, out_sites[sitename])

            # save site rectangle information [x, y, w, h, sitesize]
            out_sites[sitename] = [x, y, w, h, sitesize]

    return out_regions, out_sites

