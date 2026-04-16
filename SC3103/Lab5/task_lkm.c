




#include <linux/init.h>
#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/interrupt.h>
#include <linux/timer.h>
#include <linux/random.h>
#include <linux/delay.h> // For udelay

static unsigned int leds[] = {4, 17, 27, 18}; // G, Y, R, BUZZ
static int current_state = 0; 
static struct timer_list state_timer;
static unsigned int btn = 11;
static int irq_num;


// Helper to set LED states
void update_hw(int g, int y, int r, int b) {
    gpio_set_value(leds[0], g);
    gpio_set_value(leds[1], y);
    gpio_set_value(leds[2], r);
    gpio_set_value(leds[3], b);
}

// Function to handle the buzzing
void buzz_red_state(void) {
    int i;
    printk(KERN_INFO "Entered red state\n");
    gpio_set_value(leds[1], 0);
    for (i = 0; i < 1000; i++) { // 1000 cycles
        gpio_set_value(leds[2], 1); // Red ON
        gpio_set_value(leds[3], 1); // Buzz ON
        udelay(1000);
        gpio_set_value(leds[3], 0); // Buzz OFF
        udelay(1000);
    }
}

void timer_callback(struct timer_list *t) {
    //unsigned int r;
    if (current_state == 0) { // Transition G -> Y
  	unsigned int r;
        current_state = 1;
        update_hw(0, 1, 0, 0);
	printk(KERN_INFO "Entered yellow state\n");
        get_random_bytes(&r, sizeof(r));
        mod_timer(&state_timer, jiffies + msecs_to_jiffies((3 + (r % 8)) * 1000));
    } 
    else if (current_state == 1) { // Transition Y -> G (timeout)
        current_state = 0;
        update_hw(1, 0, 0, 0);
	printk(KERN_INFO "Timeout, entered green state\n");
        mod_timer(&state_timer, jiffies + msecs_to_jiffies(2000));
    }
    else if (current_state == 2) { // Transition R -> G
        current_state = 0;
        update_hw(1, 0, 0, 0);
	printk(KERN_INFO "Interrupt serviced, entering green state\n");
        mod_timer(&state_timer, jiffies + msecs_to_jiffies(2000));
    }
}

static irq_handler_t btn_isr(unsigned int irq, void *dev_id) {
    if (current_state == 1){
        current_state = 2;
        // In a real driver, we'd use a workqueue, but for a lab:
        buzz_red_state(); 
        // Manually trigger the transition back to Green after buzz
        mod_timer(&state_timer, jiffies + msecs_to_jiffies(10)); 
    }
    return (irq_handler_t) IRQ_HANDLED;
}

static int __init sm_init(void) {
    int i;
    for(i=0; i<4; i++) { gpio_request(leds[i], "led"); gpio_direction_output(leds[i], 0); }
    gpio_request(btn, "btn"); gpio_direction_input(btn);
    
    irq_num = gpio_to_irq(btn);
    if (request_irq(irq_num, (irq_handler_t)btn_isr, IRQF_TRIGGER_RISING, "sm_handler", NULL)){
	printk(KERN_ERR "LKM: cannot register IRQ %d\n", irq_num);
	return -EIO;
    }

    timer_setup(&state_timer, timer_callback, 0);
    current_state = 0;
    update_hw(1, 0, 0, 0);
    mod_timer(&state_timer, jiffies + msecs_to_jiffies(2000));
    
    return 0;
}

static void __exit sm_exit(void) {
    int i;
    del_timer(&state_timer);
    free_irq(irq_num, NULL);
    for(i=0; i<4; i++) { gpio_set_value(leds[i], 0); gpio_free(leds[i]); }
    gpio_free(btn);
}

module_init(sm_init);
module_exit(sm_exit);
MODULE_LICENSE("GPL");
