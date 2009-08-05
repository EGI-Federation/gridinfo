  <div id="listfiles" <?php if (!$CFG->showlistfiles) echo 'style="display:none"' ?>>
    <table>
    <tr><th>Files</th><th>Commands</th></tr>
<?php
// List files
if ($handle = opendir($CFG->dir)) {
  $count = 0;
  while (false !== ($file = readdir($handle))) {
    if ($file != "." && $file != "..") { 
      echo '<tr><td>'.$file.'</td>
      <td><a href="'.$CFG->dir.'/'.$file.'">Show</a> 
      <a href="index.php?file='.$count.'&amp;edit=true">Edit</a> 
      <a href="index.php?file='.$count.'&amp;delete=true" onclick="return confirm(\'Are you sure you want to delete it?\');" >Delete</a> 
      </td></tr>'."\n";
    }
    $count++;
  }
  closedir($handle);
}
?>
    </table>
  <p><a href="#" onclick="toggleview('newfile')">Create a new file</a></p>
  </div>

