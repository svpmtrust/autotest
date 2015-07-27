import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.io.File;
import java.io.IOException;
import java.awt.image.DataBufferByte;

class PixelArray{
    public static void main(String[] args) throws IOException
    {
	BufferedImage walle = ImageIO.read(new File("red.png"));
	final byte[] pixels = ((DataBufferByte) walle.getRaster().getDataBuffer()).getData();
	int width = walle.getWidth();
	int height = walle.getHeight();
	
	RGB[][] img = new RGB[width][height];

	final int pixelLength = 3;
	for(int pixel = 0, row = 0, col = 0; pixel < pixels.length; pixel += pixelLength)
	    {	
		
		int alpha = 0;//-16777216;
		img[col][row] = new RGB(); 
		img[col][row].r = (((int) pixels[pixel + 2] & 0xff) ) + alpha; // red
		img[col][row].g = (((int) pixels[pixel + 1] & 0xff)) + alpha; //green
		img[col][row].b = ((int) pixels[pixel] & 0xff)  + alpha; //blue
		col++;

		if (col == width) {
			col = 0;
		    row++;
		}
	    }

		//System.out.println(pixels.length);

   
     }
}

class RGB{
    int r,g,b;
}
