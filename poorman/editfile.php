<?php
// Read file content
if ($_REQUEST['file'] and $handle = opendir($CFG->dir)) {
  for ($i = 0; $i <= $_REQUEST['file']; $i++) { $file = readdir($handle); }
  closedir($handle);
}
?>
  <div id="editfile" <?php if (!$CFG->showeditfile) echo 'style="display:none"' ?>>
    <h2><?php echo $file; ?></h2>
    <p>Line format: [IDENTIFIER] [URL]</p>
    <form action="index.php" method="post">
      <input type="hidden" id="file" name="file" value="<?php echo $_REQUEST['file']; ?>" />
      <textarea rows="30" cols="80" name="updatedfile">
<?php
// Read file content
if ($_REQUEST['file'] and $handle = opendir($CFG->dir)) {
  for ($i = 0; $i <= $_REQUEST['file']; $i++) { $file = readdir($handle); }
  readfile("$CFG->dir/$file");
  closedir($handle);
}
?>
</textarea>
      <div id="button">
        <input type="submit" name="save" value="Save" onclick="return confirm('Are you sure you want to save it?');" />
        <input type="submit" value="Cancel" onclick="toggleview('listfiles'); toggleview('editfile');"/>
      </div>
    </form>
  </div>
