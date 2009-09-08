<?php
require_once('../../Datalib.php');

// Parameters
unset($CFG);
global $CFG;
$CFG->ip = $_SERVER['SERVER_ADDR'];
$CFG->referer = $_SERVER['HTTP_REFERER'];
$CFG->db = new Datalib('../../deploystats.xml');

// Check if needed files exist
foreach (array('siteName', 'public', 'contactName', 'contactEmail', 'country',
    'release', 'notifications', 'url') as $x) {
  if (! $_REQUEST[$x]) {
    $CFG->title = 'Error';
    $CFG->msg = "<p>The inserted values are not correct.</p><p>Take special attention to the field '<strong>$x</strong>'.</p><p>Go <a href=\"#\" onClick=\"history.go(-1)\">Back</a>  and try again.</p>";
    include('template.html');
    exit;
  }
}

// Insert in the db
if (! $CFG->db->exists($CFG->ip, $_REQUEST['url'])) {
  if ($CFG->db->insert($CFG->ip, $_REQUEST['url'], $_REQUEST['siteName'],
        $_REQUEST['country'], $_REQUEST['public'], $_REQUEST['contactName'],
        $_REQUEST['contactEmail'], $_REQUEST['release'], $_REQUEST['notifications']
      )) {
    $CFG->title = 'OK';
    $CFG->msg = "Congratulations! You are in!";
    include('template.html');
  } else {
    $CFG->title = 'Error';
    $CFG->msg = "There was a problem inserting your request in the database, please try a few minutes later";
    include('template.html');
  }
} else {
    $CFG->title = 'Already in the database';
    $CFG->msg = "Your IP and URL already exist in the database. If you wanna make any change, please contact the GStat support list.";
    include('template.html');
}

// Send email (future development, needs sendmail)
/*
$to = "";
$subject = "";
$body = "";
if (mail($to, $subject, $body)) {
  echo("<p>Message successfully sent!</p>");
 } else {
  echo("<p>Message delivery failed...</p>");
 }
*/
?>
