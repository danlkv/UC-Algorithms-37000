///////////////////////////////////////////////////////////////////////////////
// You need to
//    1. Read the programming assignment in homework #1.
//    2. Implement function GetStudentName.
//    3. Implement function MaxSumProduct
//    4. Compile and test your algorithm on small and large unit tests, 
//       as described in the Instructions
//    6. Fix any errors your programs may have. 
//    7. Make sure that your program does not have any memory leaks.
//    8. Remove all commented out code (that you added). 
//    0. Double check that your program does not
//       print any debug information on the screen.
//    8. Submit your code ("student_code_1.h") via Canvas.
///////////////////////////////////////////////////////////////////////////////

//required libraries
#include <string>
#include <vector>

//you can include standard C++ libraries here

// This function should return your name.
// The name should match your name in Canvas

//#define REPLIT_TEST "small"
#define REPLIT_TEST "large"

void GetStudentName(std::string& your_name)
{
   //replace the placeholders "Firstname" and "Lastname"
   //with you first name and last name
   your_name.assign("Danylo Lykov");
}

int U(const std::vector<int> &a, const std::vector<int> &T, int N)
{
  int m = 0;
  int an = a[N];
  for (int k=1; k < N+1; k++){
    // - A small performance optimization
    if (an*a[N-k] < 0)
      continue;
    // -
    // * These two lines will make the program scale as O(n) instead 
    // of O(n^2). An elegant approach for approximate solution.
    // The smaller the threshhold, the less optimal is the algorithm.
    if (k > 100)
      break;
    // *
    int m1 = T[N-k] + a[N-k]*an;
    if (m1 > m){
      m = m1;
    }
  }
  return m;
}

int MaxSumProduct(const std::vector<int>& a)
{
  int N = a.size();
  std::vector <int> T(N+1, 0);
 
  for (int i=2; i < N+1; i++){
    T[i] = std::max(U(a, T, i-1), T[i-1]);
  }
  return T[N];
}

