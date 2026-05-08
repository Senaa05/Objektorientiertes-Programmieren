# Test Case: Login Functionality

## 1. Test Case ID
**TC_001**

## 2. Test Case Title/Description
**User Login Authentication - Verify that users can successfully authenticate with valid credentials and access the library dashboard.**

## 3. Preconditions
- NiceGUI application is running on http://127.0.0.1:8080
- Database contains test users:
  - Username: "lilly2", Role: "Benutzer"
  - Username: "admin1", Role: "Admin"
- Mock database is properly initialized
- Web browser is available and can access the application URL

## 4. Test Steps
1. Open web browser and navigate to http://127.0.0.1:8080
2. Verify login page is displayed with:
   - Title "📚 Bibliothek"
   - Username input field
   - Password input field
   - "Anmelden" (Login) button
   - Test account information displayed
3. Enter valid username "lilly2" in the username field
4. Enter any password (since mock database accepts any password for test users)
5. Click the "Anmelden" button
6. Verify successful navigation to dashboard page
7. Verify user information is displayed in the header
8. Verify appropriate tabs are visible based on user role

## 5. Test Data/Input
- **Valid Test User 1:**
  - Username: "lilly2"
  - Password: "test123" (any password works in mock)
  - Expected Role: "Benutzer"
  
- **Valid Test User 2:**
  - Username: "admin1" 
  - Password: "admin123" (any password works in mock)
  - Expected Role: "Admin"

- **Invalid Test Data:**
  - Username: "nonexistent"
  - Password: "anypassword"

## 6. Expected Result
**For Valid Credentials:**
- Login succeeds without errors
- User is redirected to /dashboard page
- Header displays: "📚 Bibliothek" and user information
- User role is correctly identified and applied
- Appropriate navigation tabs are shown:
  - For "Benutzer": "Bücher" and "Meine Ausleihen" tabs
  - For "Admin": "Bücher", "Meine Ausleihen", and "Admin" tabs
- No error messages are displayed

**For Invalid Credentials:**
- Login fails
- User remains on login page
- Appropriate error message is displayed
- No access to dashboard is granted

## 7. Actual Result
*To be filled during test execution*

## 8. Status
*To be marked after test execution*
- [ ] PASS
- [ ] FAIL

## 9. Comments
**Test Environment:**
- Browser: Chrome/Firefox/Safari
- OS: macOS
- Application Version: v1.0
- Test Date: [Date of execution]

**Additional Notes:**
- Mock database accepts any password for existing users
- Test accounts are hardcoded in the UI application
- Session management should be verified (user stays logged in when navigating)
- UI responsiveness should be checked on different screen sizes
- Error handling should be tested with various invalid inputs

**Known Issues:**
- Password validation is bypassed in mock implementation
- No password hashing implemented in test environment
- Session timeout not implemented in current version

**Defects Found:**
*To be documented if any issues are discovered during testing*
