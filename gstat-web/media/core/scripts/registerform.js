/*
    Document   : Register Form
    Author     : David.Horat@cern.ch
    Description:
        Javascript validation for the register form of the DeployStats project.
        Based on jsval.js Javascript Validation library.
*/

function initValidation() {
  var objForm = document.forms["registrationform"];
  objForm.siteName.required = 1;
  objForm.siteName.realname = 'Site Name';

  objForm.url.required = 1;
  objForm.url.realname = 'URL for GStat';

  objForm.country.required = 1;
  objForm.country.exclude = '-1';
  objForm.country.realname = 'Country';

  objForm.whatIsPublic.required = 1;
  objForm.whatIsPublic.exclude = '-1';
  objForm.whatIsPublic.realname = 'Public directory';

  objForm.contactName.required = 1;
  objForm.contactName.realname = 'Contact Name';

  objForm.contactEmail.required = 1;
  objForm.contactEmail.regexp = "JSVAL_RX_EMAIL";
  objForm.contactEmail.realname = 'Contact Email address';

  objForm.notifications.required = 1;
  objForm.notifications.exclude = '-1';
  objForm.notifications.realname = 'Email notifications';
}
