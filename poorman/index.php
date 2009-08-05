<?php require_once('lib.php') ?>

<?php
// Parameters
unset($CFG);
global $CFG;
$CFG->dir = 'files'; // Directory where files are stored
$CFG->backup = 'backup'; // Directory where files are stored
$CFG->showlistfiles = true;
$CFG->shownewfile = false;
$CFG->showeditfile = false;
$CFG->user = $_SERVER['PHP_AUTH_USER'];
$CFG->logfile = 'log/actions.log';
$CFG->linkdir = 'http://grid-deployment.web.cern.ch/grid-deployment/bdii/';

///////////////////////////////////////////////////////////////
// CRUD operations
///////////////////////////////////////////////////////////////

// Delete a file
if ($_REQUEST['delete'] and $handle = opendir($CFG->dir)) {
  if ($_REQUEST['file'] == null) { die("no file specified to delete"); }
  for ($i = 0; $i <= $_REQUEST['file']; $i++) { $file = readdir($handle); }
  backup($file);
  unlink("$CFG->dir/$file") or die("unable to delete the file $file");
  $CFG->showlistfiles = true;
  $CFG->shownewfile = false;
  $CFG->showeditfile = false;
  $_REQUEST['file'] = false;
  logger('deleted', "$CFG->dir/$file");
}

// Edit a file
if ($_REQUEST['edit']) {
  $CFG->showlistfiles = false;
  $CFG->shownewfile = false;
  $CFG->showeditfile = true;
}

// Create a new file
if ($_REQUEST['create'] and $handle = opendir($CFG->dir)) {
  $filename = $_REQUEST['filename'];
  $fh = fopen("$CFG->dir/$filename", 'x') or die("can't create file $filename");
  fclose($fh);
  $handle = opendir($CFG->dir);
  $count = 0; $file = null;
  while (readdir($handle) != $file) { $count++; }
  $_REQUEST['file'] = $file;
  $CFG->showlistfiles = true;
  $CFG->shownewfile = false;
  $CFG->showeditfile = false;
  logger('created', "$CFG->dir/$filename");
}

// Save a file
if ($_REQUEST['save'] and $handle = opendir($CFG->dir)) {
  if (!$_REQUEST['file']) { die('no file specified to save'); }
  for ($i = 0; $i <= $_REQUEST['file']; $i++) { $file = readdir($handle); }
  backup($file);
  $fh = fopen("$CFG->dir/$file", 'w') or die("can't open file $file to write");
  fwrite($fh, $_REQUEST['updatedfile']); fclose($fh); closedir($handle);
  $CFG->showlistfiles = true;
  $CFG->shownewfile = false;
  $CFG->showeditfile = false;
  logger('updated', "$CFG->dir/$file");
}
?>

<?php include('header.php') ?>
<?php include('listfiles.php') ?>
<?php include('newfile.php') ?>
<?php if ($_REQUEST['file']) include('editfile.php'); ?>
<?php include('footer.php') ?>
