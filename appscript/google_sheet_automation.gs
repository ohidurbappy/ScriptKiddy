var ss = SpreadsheetApp.openById("ID of the Sheet created above");
var sheet = ss.getSheetByName("Sheet1");

function createMontlySheet(){
  
  var cur_month = Utilities.formatDate(new Date(),"IST", "MMMM YYYY");
  
  var new_monthly_sheet = SpreadsheetApp.create("Attendance Sheet "+cur_month);
  
  var sheet_file = DriveApp.getFileById(new_monthly_sheet.getId());
  
  var cur_folder = DriveApp.getFolderById("1XSCzAWu1OyJxwwLPfpxLwjJbjHd4WWfv");
  
  cur_folder.addFile(sheet_file);
  
  sheet.getRange(3,2).setValue(new_monthly_sheet.getId());
  
}

function dailyDump(){
  
  var dss = SpreadsheetApp.openById(sheet.getRange(2,2).getValue());
  
  var mss = SpreadsheetApp.openById(sheet.getRange(3,2).getValue());
  
  var daily_sheet = dss.getSheetByName("daily_attendance");
  
  var copied_sheet = daily_sheet.copyTo(mss);
  
  copied_sheet.setName(new Date().getDate());
  
  daily_sheet.clear();
  
  
}
