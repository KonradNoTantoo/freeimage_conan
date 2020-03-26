#include <iostream>
#include "FreeImage.h"

int main()
{
	FreeImage_Initialise();
	std::cout << "FreeImage " << FreeImage_GetVersion() << ", with:" << std::endl;

	for (int i = 0; i < FreeImage_GetFIFCount(); ++i)
	{
		std::cout << "\t- " << FreeImage_GetFIFExtensionList((FREE_IMAGE_FORMAT)i) << std::endl;
	}

	FreeImage_DeInitialise();
	return 0;
}
