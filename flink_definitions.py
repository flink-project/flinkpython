__author__ = "Urs Graf"
__license__ = "http://www.apache.org/licenses/LICENSE-2.0"
__version__ = "1.0"

REGISTER_WIDTH		        = 4		                # in byte                      
REGISTER_WIDTH_BIT	        = REGISTER_WIDTH * 8	                 
HEADER_SIZE		            = 16                    # in byte                      
SUBHEADER_SIZE	            = 16            		# in byte                      
TOTAL_HEADER_SIZE           = HEADER_SIZE + SUBHEADER_SIZE
                                                                    
TYPE_OFFSET                 = 0x0         
SIZE_OFFSET                 = 0x4                                
CHANNEL_OFFSET              = 0x8                                 
UNIQUE_ID_OFFSET            = 0xC                                 
MOD_STATUS_OFFSET           = 0x10                                
MOD_CONF_OFFSET             = 0x14    

INFO_DESC_SIZE              = 28                    # in byte
                                                                    
INFO_INTERFACE_ID           = 0x00                                
ANALOG_INPUT_INTERFACE_ID   = 0x01   
ANALOG_OUTPUT_INTERFACE_ID  = 0x02                                
GPIO_INTERFACE_ID           = 0x05;                                
COUNTER_INTERFACE_ID        = 0x06;                                
PWM_INTERFACE_ID            = 0x0C;                                
PPWA_INTERFACE_ID           = 0x0D;                                
UART_INTERFACE_ID           = 0x0F;                                
WD_INTERFACE_ID             = 0x10;                                
                                                                    
INTERFACE_TYPE_MASK         = 0xFFFF;                              
INFO_DEVICE_SIZE            = 0x80;           