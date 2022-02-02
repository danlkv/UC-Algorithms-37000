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
  for (int k=1; k < N+1; k++){
    int m1 = T[N-k] + a[N-k]*a[N];
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

