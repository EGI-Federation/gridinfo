<?php

# http://code.google.com/p/cssmin/

include('cssmin.php');

if ($argc > 1) {

  $file = $argv[1];
  file_put_contents($file, cssmin::minify(file_get_contents($file)));

}
?>
