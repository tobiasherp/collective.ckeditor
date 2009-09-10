# -*- coding: UTF-8 -*-
# Authors: 
#!/usr/bin/env python
#BOILERPLATE###################################################################
#                                                                             #
#  This package wraps FCKeditor for use in the Zope web application server.   #
#  Copyright (C) 2005 Chad Whitacre < http://www.zetadev.com/ >               #
#                                                                             #
#  This library is free software; you can redistribute it and/or modify it    #
#  under the terms of the GNU Lesser General Public License as published by   #
#  the Free Software Foundation; either version 2.1 of the License, or (at    #
#  your option) any later version.                                            #
#                                                                             #
#  This library is distributed in the hope that it will be useful, but        #
#  WITHOUT ANY WARRANTY; without even the implied warranty of                 #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser    #
#  General Public License for more details.                                   #
#                                                                             #
#  You should have received a copy of the GNU Lesser General Public License   #
#  along with this library; if not, write to the Free Software Foundation,    #
#  Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA                #
#                                                                             #
#                                                                             #
###################################################################BOILERPLATE#

""" This script takes the FCKeditor base distribution in ../src/ and massages it
for use in Zope, outputting to ../skins/fckeditor/. Usage:

    $ ./base2zope.py
    $

"""

import os
import re
import shutil
import sys
import codecs


##
# Initialize some variables.
##

PRODUCT_ROOT = os.path.realpath(os.path.join(sys.path[0],'..'))
SRC_ROOT     = os.path.join(PRODUCT_ROOT, '_src', 'ckeditor')
DEST_ROOT    = os.path.join(PRODUCT_ROOT, 'browser', 'ckeditor')
SRC_SKINS_ADDONS_ROOT = os.path.join(PRODUCT_ROOT, '_addons','skins')
DEST_SKINS_ADDONS_ROOT = os.path.join(PRODUCT_ROOT, 'browser','ckeditor','skins')
SRC_PLUGINS_ADDONS_ROOT = os.path.join(PRODUCT_ROOT, '_addons','plugins')
DEST_PLUGINS_ADDONS_ROOT = os.path.join(PRODUCT_ROOT, 'browser','ckeditor','plugins')


##
# Decide what to do if DEST_ROOT is already there.
##

def rm_rf(path):
    """ equivalent to rm -rf on Unix
    """
    if os.path.realpath(path) == '/':
        print 'will not rm -rf /' # better safe than sorry :-)
        sys.exit(1)
    else:
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

if os.path.exists(DEST_ROOT):
    force = sys.argv[1:2] == ['--force']
    if not force:
        answer = raw_input( "destination directory already exists; " +\
                            "delete and recreate? (y/n) [n] "
                            )
        force = answer.lower() == 'y'
    if force:   rm_rf(DEST_ROOT)
    else:       sys.exit(1)
else:
    os.makedirs(DEST_ROOT)




ext_unwanted = ('asp','aspx','cfc','cfm','cgi','exe','htaccess','php','pl','lasso','afp')
# files overloaded
files_unwanted = ()
# files changed 
files_changed = {}


def makeSkinDirs(srcDir ,destDir):
  """
  Now walk the tree and transfer data to our output directory.
  """
  for path, dirs, files in os.walk(srcDir):
  
      # Determine and maybe create the destination.
      relpath = path[len(srcDir)+1:]
      destpath = os.path.join(destDir, relpath)
      if not os.path.exists(destpath):
          os.mkdir(destpath)
  
      for filename in files:
  
          ext = filename.split('.')[-1]
          
          src = os.path.join(path, filename)
  
          dest = os.path.join(destpath, filename)
  
          # Create the new file if we want it.
          if ext not in ext_unwanted and filename not in files_unwanted:                                                               
                          
              if files_changed.has_key(filename) :
  
                  # TODO : add Title, description, and image sizes fileds in direct upload forms
                  pass

              # reduce a big frame in WSC Spellchecker (beurk)
              elif filename=='tmpFrameset.html':
                  inputfile = file(src)
                  outputfile = file(dest, 'w+')
                  for line in inputfile.readlines():
                      if "parseInt( oParams.thirdframeh, 10 )" in line :
                          newline = '    sFramesetRows = "27,*," + ( parseInt( oParams.thirdframeh, 10 ) || "150" ) + ",0" ;\r'
                          outputfile.write(newline)                                
                      else:
                          outputfile.write(line)
                          
                  inputfile.close()
                  outputfile.close()
     
  
              else:
                  shutil.copy(src, dest)
                  
              #remove BOM, a known bug on some fckeditor versions (ex: http://sourceforge.net/tracker/index.php?func=detail&aid=1685547&group_id=75348&atid=543653)
              if filename.endswith('.html'):
                  fileObj = codecs.open( dest, "r", "utf-8" ) 
                  u = fileObj.read()   
                  fileObj.close()                        
                  if u.startswith( unicode( codecs.BOM_UTF8, "utf8" ) ) :      
                     fileObj = codecs.open( dest, "w", "utf-8" )
                     fileObj.write(u.lstrip(unicode( codecs.BOM_UTF8, "utf8" )))       
                     fileObj.close()
                              
              if destpath.endswith('_samples') and  ext=='html' :
                  fileObj = file(dest) 
                  content = fileObj.read()   
                  fileObj.close()  
                  # put good base href + basehref IE fix for samples (bug ckeditor 3.0)
                  content = content.replace('<head>','<head>\n  <base href="./" /><!--[if lt IE 7]></base><![endif]-->')
                  fileObj = file(dest,"w")
                  fileObj.write(content)
                  fileObj.close()       
              
              # fix xhtml compilation error
              if ext in ('html', 'xml', 'pt') :
                  fileObj = file(dest) 
                  content = fileObj.read()   
                  fileObj.close()  
                  # TODO : use a regexp (replace /option by any tag)
                  content = content.replace("'</option>'","'<\/option>'")
                  fileObj = file(dest,"w")
                  fileObj.write(content)
                  fileObj.close()                    

  
      # skip svn directories
      if '.svn' in dirs:
          dirs.remove('.svn')
  

#Add base skin directory
makeSkinDirs(SRC_ROOT ,DEST_ROOT)
# TODO :  Add new skins and plugins
# makeSkinDirs(SRC_SKINS_ADDONS_ROOT,DEST_SKINS_ADDONS_ROOT)
# makeSkinDirs(SRC_PLUGINS_ADDONS_ROOT,DEST_PLUGINS_ADDONS_ROOT)