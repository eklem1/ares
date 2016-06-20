#!/usr/bin/env python

import os, re, urllib, sys, tarfile

options = sys.argv[1:]

ares_link = 'https://bitbucket.org/mirochaj/ares'
         
# Auxiliary data downloads
# Format: [URL, file 1, file 2, ..., file to run when done]

aux_data = \
{
 'hmf': ['%s/downloads' % ares_link, 
    'hmf_ST_logM_1200_4-16_z_1141_3-60.pkl',
    None],
 'inits': ['%s/downloads' % ares_link, 
     'initial_conditions.npz',
     None],    
 'optical_depth': ['%s/downloads' % ares_link, 
    'optical_depth_H_400x1616_z_10-50_logE_2-4.7.pkl',
    'optical_depth_He_400x1616_z_10-50_logE_2-4.7.pkl',
    None],
 'secondary_electrons': ['http://www.astro.ucla.edu/~sfurlane/docs',
    'elec_interp.tar.gz', 
    'read_FJS10.py'],
 'starburst99': ['http://www.stsci.edu/science/starburst99/data',
    'data.tar.gz', 
    None],                        
 'hm12': ['http://www.ucolick.org/~pmadau/CUBA/Media',
    'UVB.out', 
    'emissivity.out', 
    None],
 'bpass_v1': ['http://bpass.auckland.ac.nz/2/files'] + \
    ['sed_bpass_z%s_tar.gz' % Z for Z in ['001', '004', '008', '020', '040']] + \
    [None],

}

os.chdir('input')

if 'minimal' in options:
    to_download = ['inits', 'secondary_electrons']
else:
    to_download = aux_data.keys()

for direc in to_download:
    if not os.path.exists(direc):
        os.mkdir(direc)
    
    os.chdir(direc)
    
    web = aux_data[direc][0]
    for fn in aux_data[direc][1:-1]:
    
        if os.path.exists(fn):
            if 'fresh' or 'clean' in options:
                os.remove(fn)
            
        if 'clean' in options:
            continue
    
        print "Downloading %s/%s..." % (web, fn)
        urllib.urlretrieve('%s/%s' % (web, fn), fn)
        
        if not re.search('tar', fn):
            continue
            
        tar = tarfile.open(fn)
        tar.extractall()
        tar.close()
    
    # Run a script [optional]
    if aux_data[direc][-1] is not None:
        execfile(aux_data[direc][-1])
    
    os.chdir('..')

