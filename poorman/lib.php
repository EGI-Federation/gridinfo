<?php
// Logger
function logger($action, $actionfile) {
  global $CFG;
  $msg = date('Y-m-d\ H:i:s U').": $action file '$actionfile' by user ".$CFG->user;
  $file = fopen($CFG->logfile, 'a+') or die("can't open log file ".$CFG->logfile);
  fwrite($file, $msg."\r\n");
  fclose($file);
}

// Backup
function backup($file) {
  global $CFG;
  $oldfilename = $CFG->dir.'/'.$file;
  $newfilename = $CFG->backup.'/'.date('U').'-'.$file;
  copy($oldfilename, $newfilename) or die("can't make a backup of $oldfilename into $newfilename");
}
?>
