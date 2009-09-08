<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
    <title>Deployment Stats</title>
    <link rel="stylesheet" type="text/css" href="example.css" />
  </head>
  <body>
    <h1>Deployment Statistics for GStat 2.0</h1>
<?php
require_once('../../Datalib.php');

// Parameters
unset($CFG);
global $CFG;
$CFG->db = new Datalib('../../deploystats.xml');

// Show
print '<table>';
$res = $CFG->db->showAccepted();
foreach ($res as $entry) {
  if ($entry->public == 'nameandlink') {
    print '<tr><td><a href="'.$entry->url.'">'.$entry->siteName.'</a></td></tr>';
  } elseif ($entry->public == 'nameonly') {
    print '<tr><td>'.$entry->siteName.'</td></tr>';
  }
}
print '</table>';
print '<p><strong>Number of sites with GStat deployed</strong>: '.count($res).'</p>';
?>
    <p>Note that only sites which wished it are shown in the table above</p>
  </body>
</html>
