function sendEndOfYearEmails() {
  var spreadSheet = SpreadsheetApp.getActiveSheet();
  var dataRange = spreadSheet.getDataRange();
  // Fetch values for each row in the Range.
  var data = dataRange.getValues();
  var text = ‘our initial sample text’;
  for (var i = 1; i < data.length; i++) {
    (function(val) {
      var row = data[i];
      var emailAddress = row[1]; //position of email header — 1
      Var name = row[0]; // position of name header — 1
      var message = ‘Dear’ + name + ‘\n\n’ + text;
      var subject = ‘Sending emails from a Spreadsheet’;
      MailApp.sendEmail(emailAddress, subject, message);
      })(i);
   }
}
