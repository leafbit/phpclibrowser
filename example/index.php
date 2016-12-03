<html>
<head>
  <title>PHP CLI Broser Scirpt Example</title>
  <style>
  .message {
    border: 1px solid green;
    background: lightgreen;
  }
  </style>
</head>
<body>
<h1>PHP Script Example</h1>

<?php
function show_message($text, $vals) {
  if (!$vals) return;
  print '<div class="message">' . $text . '<br />';
  print_r($vals);
  print '</div>';
}
// If anything send by $_POST or $_GET - show:
show_message('A post event received. It contains:', $_POST);
show_message('A get event received. It contains:', $_GET);
echo '<p>A random number: ' . rand(0, 999999) . '</p>';
?>

<p>
<a href="index.php?argument=daa&andarg=noo">Test Link</a> - click on this link to test get method.
</p>

<p>
  An example of form to test GET method:
</p>
    <form action="index.php">
    <table>
    <tbody>
      <tr>
        <td>First name:</td>
        <td><input type="text" name="person[firstname]" value="Ali"></td>
      </tr>
      <tr>
        <td>Last name:</td>
        <td><input type="text" name="person[lastname]" value="Bl'ahblah&"></td>
      </tr>
      <tr>
        <td>Gender:</td>
        <td>
          <input type="radio" name="gender" value="Male" checked="checked"> Male
          <input type="radio" name="gender" value="Female"> Female
          </td>
      </tr>
      <tr>
        <td>Source:</td>
        <td><select name="source">
          <option>Sand</option>
          <option>Water</option>
          <option>Fire"</option>
          <option>Earth</option>
          <option>Wood</option>
          <option>Milk</option>
          </select>
          </td>
      </tr>
      <tr>
        <td colspan="2">
          <input type="checkbox" name="checkboxtest" value="receive">
          Checkbox test
          </td>
      </tr>
      <tr>
        <td colspan="2">
          <textarea name="multiline" cols=60 rows=6>
This is a long long story. Years and years ago
before computers and other electronic hardware
existed one script written on stone plates.

It was well formatted, well compiled and well done.
So what?
          </textarea>
          </td>
      </tr>
      <tr>
        <td>Upload Something?</td>
        <td><input type="file" name="afile" /></td>
      </tr>
    </tbody>
    </table>
    <input type="submit" value="Submit this now!">
    </form>
<p>
  An example of form to test POST method:
</p>
    <form action="index.php" method="POST" enctype="multipart/form-data">
     <table>
    <tbody>
      <tr>
        <td>First name:</td>
        <td><input type="text" name="firstname" value="Aliya"></td>
      </tr>
      <tr>
        <td>Last name:</td>
        <td><input type="text" name="lastname" value="Blahblaha"></td>
      </tr>
      <tr>
        <td>Gender:</td>
        <td>
          <input type="radio" name="gender" value="Male"> Male
          <input type="radio" name="gender" value="Female" checked="checked"> Female
          </td>
      </tr>
      <tr>
        <td>Source:</td>
        <td><select name="source">
          <option>Sand</option>
          <option>Water</option>
          <option selected=selected>Fire</option>
          <option>Earth</option>
          <option>Wood</option>
          <option>Milk</option>
           </select>
            </td>
      </tr>
      <tr>
        <td colspan="2">
          <input type="checkbox" name="checkboxtest" value="receive">
          Checkbox test
          </td>
      </tr>
      <tr>
        <td colspan="2">
          <textarea name="multiline" cols=60 rows=6>
This is a long long story. Years and years ago
before computers and other electronic hardware
existed two script written on golden plates.

It was well formatted, well compiled and well done.
So... one day it got run.
          </textarea>
          </td>
      </tr>
      <tr>
        <td>Upload this too?</td>
        <td><input type="file" name="afile2" />
No no no - it will result in C:\fakepath\urfilename
</td>
      </tr>
    </tbody>
    </table>
    <input type="submit" value="Submit me! Test Me!">
   </form>
</body>
</html>
