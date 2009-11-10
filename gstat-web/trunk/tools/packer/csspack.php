<?php

# http://code.google.com/p/cssmin/

include('cssmin.php');

if ($argc > 1) {

  $file = $argv[1];
  $output = cssmin::minify(file_get_contents($file));
  fwrite(STDOUT, $output);

}
?>
