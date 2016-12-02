<html><body>
<h1>
The Green People Book Club
</h1>

<?php
if ($_POST) {
  print_r($_POST);
}
?>

<p>
Welcome to The Green People Book Club. Please register to obtain a membership with us.
</p>
    <form action="index.php" data-onsubmit="phpBrowser.submit(this);return false;">
    <table>
    <tbody><tr>
        <td>
        First name:
        </td>
        <td>
            <input type="text" name="firstname" id="firstname">
        </td>
    </tr>
    <tr>
        <td>
        Last name:
        </td>
        <td>
            <input type="text" name="lastname" id="lastname">
        </td>
    </tr>
    <tr>
        <td>
        Gender:
        </td>
        <td>
        <input type="radio" name="gender" id="genderMale" value="Male"> Male
        <input type="radio" name="gender" id="genderFemale" value="Female"> Female
        </td>
    </tr>
    <tr>
        <td colspan="2">
        <input type="checkbox" name="updates" id="updates" value="receive">
        Check here if you would like to receive regular updates from us:
        </td>
    </tr>
    </tbody></table>
    <input type="submit" value="Submit">
    </form>

    <p>
    <a href="another.php?argument=daa&andarg=noo">Test Link</a>
    </p>
    <script>
    function IWantToDo(){
      formExtractor.goto('This is where I want to go');
    }
    </script>
    <input type="button" onclick="IWantToDo()" value="Shmksss" />
</body></html>
