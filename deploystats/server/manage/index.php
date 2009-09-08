<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Deployment Stats</title>
    <link rel="stylesheet" type="text/css" href="example.css" />
  </head>
  <body>
    <h1>Deployment Statistics for GStat 2.0</h1>
    <h2>Manager panel</h2>
    <h3>New entries</h3>
<?php
require_once('../../Datalib.php');

// Parameters
unset($CFG);
global $CFG;
$CFG->db = new Datalib('../../deploystats.xml');

// Show
print '<table border="1">';
$res = $CFG->db->showNew();
foreach ($res as $entry) {
  print '<tr><td>'.$entry->siteName.'</td></tr>';
}
print '</table>';
print '<p>Number of new sites: '.count($res).'</p>';
?>

    <h3>Denied entries</h3>
<?php
print '<table border="1">';
$res = $CFG->db->showDenied();
foreach ($res as $entry) {
  print '<tr><td>'.$entry->siteName.'</td></tr>';
}
print '</table>';
print '<p>Number of denied sites: '.count($res).'</p>';
?>
  </body>
</html>
