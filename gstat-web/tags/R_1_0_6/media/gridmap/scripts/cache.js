// This file is part of the GridMap software (see http://gridmap.cern.ch)
// Copyright (c) EDS and CERN 2007, patent pending
//
// Author: Max Boehm, max.boehm@eds.com, max.boehm@cern.ch
//
// History:
// 18.09.2007  mb        created
//


function Cache(maxentries)
{
    // public members
    this.maxentries = maxentries;
    this.cache = {};                // {key: {obj:obj, lastaccess:ts, expires:ts} }

    // - key       unique string
    // - obj       object to cache for given key
    // - lifetime  seconds, until cache entry expires
    this.add = function(key, obj, lifetime)
    {
        if (!this.cache.hasOwnProperty(key)) {
            var oldestkey = null;
            var count = 0;
            for (var k in this.cache) {
                if (this.cache.hasOwnProperty(k)) {
                    count = count+1;
                    if (!oldestkey || this.cache[k].lastaccess<this.cache[oldestkey].lastaccess) {
                        oldestkey = k;
                    }
                }
            }
            if (count>=this.maxentries) {
                delete this.cache[oldestkey];       // remove oldest entry
            }
        }

        // save new entry
        var now = (new Date()).getTime();
        this.cache[key] = {obj:obj, lastaccess:now, expires:now+lifetime*1000};
    };

    // returns
    // - cache entry, if entry is available and not expired
    // - null otherwise
    this.get = function(key)
    {
        if (this.cache.hasOwnProperty(key)) {
            var entry = this.cache[key];
            var now = (new Date()).getTime();
            if (now>=entry.lastaccess && now<entry.expires) {
                // entry is valid
                entry.lastaccess = now;
                return entry.obj;
            }
            delete this.cache[key];     // remove expired entry from cache
        }
        return null;
    };
}
