<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
  <title>BDII Web Config</title>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-15" />
  <link rel="icon" href="" type="image/png" />
  <link rel="shortcut icon" href="" type="image/png" />
  <meta name="lang" content="en" />
  <meta name="author" content="David Horat" />
  <meta name="organization" content="CERN" />
  <meta name="locality" content="Geneva, Switzerland" />
  <meta name="keywords" content="BDII, EGEE, WLCG, Grid, CERN, BDII Web Config" />
  <meta name="description" content="BDII config files editor" />
  <meta http-equiv="Pragma" content="no-cache" />
  
  <link rel="stylesheet" href="bdii.css" type="text/css" media="all" />
  
  <script type="text/javascript">
  function toggleview(element1) {
     element1 = document.getElementById(element1);
     if (element1.style.display == 'block' || element1.style.display == '')
        element1.style.display = 'none';
     else
        element1.style.display = 'block';
     return;
  }
  </script>

</head>
<body>
  <div id="welcome">Welcome, <b><?php echo substr($CFG->user, strrpos($CFG->user, '=') + 1); ?></b></div>
  <div id="Content">
  <h1>BDII Web Config</h1>
