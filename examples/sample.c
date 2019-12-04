int main() {
  int a;
  char buffer[5], str[5];
  scanf_s("%d", &a);

  if (a == 1) {
    if (a == 2) {
      gets(buffer);
    }
    else {
      gets(buffer);
      strcpy(str, buffer);
    }
  }
  else {
    if (a == 1) {
      strcat(buffer, str);
    }
  }
  
  return 0;  
}