#include <iostream>
#include "FreeImage.h"

int main()
{
	FreeImage_Initialise();
	std::cout << "FreeImage " << FreeImage_GetVersion() << std::endl;
	FreeImage_DeInitialise();
	return 0;
}
