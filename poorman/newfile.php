  <div id="newfile" <?php if (!$CFG->shownewfile) echo 'style="display:none"' ?>>
    <form action="index.php" method="post">
      <input type="text" id="filename" name="filename" />
      <input type="submit" name="create" value="Create" />
    </form>
  </div>

