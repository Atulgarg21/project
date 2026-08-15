import java.util.Scanner;
public class Main
{
	public static void main(String[] args) {
		System.out.println("select operation\n 1 for addition\n 2 for subtraiton\n 3 for multiply\n 4 for divide");
		Scanner sc = new Scanner(System.in);
		int choice = sc.nextInt();
		System.out.println("give first number");
		int a = sc.nextInt();
		System.out.println("give second number");
		int b = sc.nextInt();
		switch (choice) {
		case 1:
			System.out.println(a+b);
			break;
		case 2:
			System.out.println(a-b);
			break;
		case 3:
			System.out.println(a*b);
			break;
		case 4:
			System.out.println(a/b);
			break;
		}
	}
}
