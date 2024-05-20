#include "phylib.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>


// Function to create a new still ball object
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {

    phylib_object *new_object = (phylib_object*)malloc(sizeof(phylib_object));

    if(new_object == NULL){
        return NULL;
    }
    //Set type to still
    new_object->type = PHYLIB_STILL_BALL;

    //function parameters to the struct
    new_object->obj.still_ball.number = number;
    new_object->obj.still_ball.pos = *pos; //!

    return new_object;
}
// Function to create a new rolling ball object
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {

    phylib_object *new_object = (phylib_object*)malloc(sizeof(phylib_object));

    if(new_object == NULL){
        return NULL;
    }

    //Set to rolling
    new_object->type = PHYLIB_ROLLING_BALL;

    new_object->obj.rolling_ball.number = number;
    new_object->obj.rolling_ball.pos = *pos; //!
    new_object->obj.rolling_ball.vel = *vel;
    new_object->obj.rolling_ball.acc = *acc;

    return new_object;

}

// Function to create a new hole object
phylib_object *phylib_new_hole(phylib_coord *pos) {

    phylib_object *new_object = (phylib_object*)malloc(sizeof(phylib_object));

    if(new_object == NULL){
        return NULL;
    }
    //Set to hole
    new_object->type = PHYLIB_HOLE;

    new_object->obj.hole.pos = *pos;

    return new_object;
}

// Function to create a new horizontal cushion object
phylib_object *phylib_new_hcushion(double y) {
    phylib_object *new_object = (phylib_object*)malloc(sizeof(phylib_object));

    if(new_object == NULL){
        return NULL;
    }
    //Set to Hcushion
    new_object->type = PHYLIB_HCUSHION;

    new_object->obj.hcushion.y = y;

    return new_object;
}

// Function to create a new vertical cushion object
phylib_object *phylib_new_vcushion(double x) {
    phylib_object *new_object = (phylib_object*)malloc(sizeof(phylib_object));

    if(new_object == NULL){
        return NULL;
    }
    //Set to Hcushion
    new_object->type = PHYLIB_VCUSHION;

    new_object->obj.vcushion.x = x;

    return new_object;
}

// Function to create a new phylib_table
phylib_table *phylib_new_table(void) {
    phylib_table *new_table= (phylib_table*)malloc(sizeof(phylib_table));

    phylib_coord lowLHole, lowRHole, medLHole, medRHole, upperLHole, upperRHole;

    lowLHole.x = 0.0;
    lowLHole.y = 0.0;

    lowRHole.x = PHYLIB_TABLE_WIDTH;
    lowRHole.y = 0.0;

    medLHole.x = 0.0;
    medLHole.y = PHYLIB_TABLE_WIDTH;

    medRHole.x = PHYLIB_TABLE_WIDTH;
    medRHole.y = PHYLIB_TABLE_WIDTH;

    upperLHole.x = 0.0;
    upperLHole.y = PHYLIB_TABLE_LENGTH;

    upperRHole.x = PHYLIB_TABLE_WIDTH;
    upperRHole.y = PHYLIB_TABLE_LENGTH;
    
    if(new_table == NULL){
        return NULL;
    }

    // Initialize the array of objects to NULL
    for (int i =0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        new_table->object[i] = NULL;
    }

    new_table->time = 0.0;

    // Add elements to the array
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    new_table->object[4] = phylib_new_hole(&lowLHole);
    new_table->object[5] = phylib_new_hole(&medLHole);
    new_table->object[6] = phylib_new_hole(&upperLHole);
    new_table->object[7] = phylib_new_hole(&lowRHole);
    new_table->object[8] = phylib_new_hole(&medRHole);
    new_table->object[9] = phylib_new_hole(&upperRHole);

    // Check if any object creation failed
    for (int i = 0; i < 10; i++)
    {
        if (new_table->object[i] == NULL)
        {
            return NULL;
        }
    }

    return new_table;
}

// Function to copy the contents of one phylib_object to another
void phylib_copy_object( phylib_object **dest, phylib_object **src ){

    if (*src == NULL){
        *dest = NULL;
        return;
    }
    *dest = (phylib_object *)malloc(sizeof(phylib_object));

    if (*dest != NULL){
        memcpy(*dest, *src, sizeof(phylib_object));
    }
}
//allocates memory for a new phylib_table and copies the contents from the original table to the new memory location.
phylib_table *phylib_copy_table(phylib_table *table) {
    if (table == NULL) 
    {
        return NULL;
    }
    //Allocate space for new table
    phylib_table *copy_table = (phylib_table *)malloc(sizeof(phylib_table));
    if (copy_table == NULL) 
    {
        free(copy_table);
        return NULL;
    }
    copy_table->time = table->time;
    // Copy each object from the original table to the new table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i ++)
    {
        if (table->object[i] != NULL) {
            phylib_copy_object(&copy_table->object[i], &table->object[i]);
        } else {
            copy_table->object[i] = NULL;
        }
    }
    return copy_table;
}

// Function to add an object to the phylib_table
void phylib_add_object( phylib_table *table, phylib_object *object ){
    //Verify that both aren't null
     if (table == NULL || object == NULL) {
        return;  // Do nothing if either table or object is NULL
    }
        //Loop through til empty slot found
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i){
                if (table->object[i] == NULL){
                    table->object[i] = object;
                    return;
                }
            }

}

// Function to free memory occupied by a phylib_table
void phylib_free_table( phylib_table *table ){
    if (table == NULL){
        return;
    }
    //Loops through freeing each object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++){
        if(table->object[i] != NULL){
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }
    //Frees the table itself
    free(table);

}

// Function to find difference between two coordinates
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){

    phylib_coord diff;

    //Calculate x & y differences
    diff.x = c1.x - c2.x;
    diff.y = c1.y - c2.y;

    return diff;
}

// Function to calculate the length of a vector
double phylib_length( phylib_coord c ){

    //Compute sqrt of the sum of products of the coordinates
    return sqrt((c.x * c.x) + (c.y * c.y));
}

// Function to calculate the dot product of two vectors
double phylib_dot_product( phylib_coord a, phylib_coord b ){

    //Return sum of coefficiant products
    return (a.x * b.x) + (a.y * b.y);

}

// Function to calculate the distance between two phylib_objects
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ){
    
    if (obj1->type != PHYLIB_ROLLING_BALL){
        return -1.0;
    }

    phylib_coord position1 = obj1->obj.rolling_ball.pos;
    phylib_coord position2;

    //Calculate distance based on obj2
    switch (obj2->type) {
        //If still or rolling ball, find distance & subtract ball diameter
        case PHYLIB_ROLLING_BALL:
        case PHYLIB_STILL_BALL:
            position2 = obj2->obj.still_ball.pos;
            return phylib_length(phylib_sub(position1, position2)) - PHYLIB_BALL_DIAMETER;
            //if hole, find its distance & subtract hole diameter
        case PHYLIB_HOLE:
            position2 = obj2->obj.hole.pos;
            return phylib_length(phylib_sub(position1, position2)) - PHYLIB_HOLE_RADIUS;
            //If cushion, find abs distance & subtract ball radius
        case PHYLIB_VCUSHION:
            return fabs(position1.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
        case PHYLIB_HCUSHION:
            return fabs(position1.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            //Else return
        default:
            return -1.0;
    }
}


// Function to update the position and velocity of a rolling ball after a certain time
void phylib_roll( phylib_object *new, phylib_object *old, double time ){
    if (new == NULL || old == NULL){
        return;
    }
    //Checks that rolling ball is passed
    if (new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL){
        return; 
    }

    //Update position x & y
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + (old->obj.rolling_ball.vel.x * time) +  
    (0.5 * old->obj.rolling_ball.acc.x * time * time);

    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + (old->obj.rolling_ball.vel.y * time) + 
    (0.5 * old->obj.rolling_ball.acc.y * time * time);

    //Update velocity x & y
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;

    //Check whether velocity changes sign, adjust new velocity & acceleration accordingly 
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0.0){
        new->obj.rolling_ball.acc.x = 0.0;
        new->obj.rolling_ball.vel.x = 0.0;
    }

    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0.0){
        new->obj.rolling_ball.acc.y = 0.0;
        new->obj.rolling_ball.vel.y = 0.0;
    }
}

// Function to check if a rolling ball has stopped, and if so, convert it to a still ball
unsigned char phylib_stopped( phylib_object *object ){

    if (object == NULL || object->type!= PHYLIB_ROLLING_BALL){
        return 0;
    }
    
    if(phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON){
    
        //Place objects's fields into temp values
        unsigned char tempNum = object->obj.rolling_ball.number;
        phylib_coord tempPos = object->obj.rolling_ball.pos;
    
        //Assign the new type
        object->type = PHYLIB_STILL_BALL;

        //Reassign
        object->obj.still_ball.number = tempNum;
        object->obj.still_ball.pos = tempPos;

        return 1;
    
    }else{
        return 0;
    }
}

// Function to handle collision between two objects
void phylib_bounce( phylib_object **a, phylib_object **b ){
    
    phylib_coord r_ab, v_rel;
    unsigned char tempNum = (*b)->obj.still_ball.number;        
    phylib_coord tempPos =  (*b)->obj.still_ball.pos;
    phylib_coord n;

    switch((*b)->type)
    {
        case PHYLIB_HCUSHION: 

            //Reverse the y velocity
            (*a)->obj.rolling_ball.vel.y = (*a)->obj.rolling_ball.vel.y * -1;
            (*a)->obj.rolling_ball.acc.y = (*a)->obj.rolling_ball.acc.y * -1;
            break;

        case PHYLIB_VCUSHION: 

            //Reverse x velocity
            (*a)->obj.rolling_ball.vel.x = (*a)->obj.rolling_ball.vel.x * -1;
            (*a)->obj.rolling_ball.acc.x = (*a)->obj.rolling_ball.acc.x * -1;
            break;

        case PHYLIB_HOLE:

            free(*a);    // Free the memory of object a
            *a = NULL;   // Set it to NULL
            break;

        case PHYLIB_STILL_BALL:
            //Convert to a rolling ball
            
            (*b)->type = PHYLIB_ROLLING_BALL;

            (*b)->obj.rolling_ball.number = tempNum;
            (*b)->obj.rolling_ball.pos = tempPos;

            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;

            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;

        case PHYLIB_ROLLING_BALL:
            // Compute the position of object a with respect to object b (r_ab)
            //phylib_coord r_ab, v_rel;
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos,(*b)->obj.rolling_ball.pos);

            // Compute the relative velocity of object a with respect to object b (v_rel)
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel,(*b)->obj.rolling_ball.vel);
        
            // Calculate the length of r_ab
            double len = phylib_length(r_ab);

            // Check if the length is not zero to avoid division by zero
            if (len != 0) {
                // Divide x and y components by the length of r_ab
                n.x = r_ab.x / len;
                n.y = r_ab.y / len;
            } else {
                // Handle the case where length is zero to avoid division by zero
                n.x = 0.0;
                n.y = 0.0;
            }

            double v_rel_n = phylib_dot_product(v_rel, n);
        
             // Update the velocities of objects a and b
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            // Compute the speed of objects a and b
            double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            double speed_b = phylib_length((*b)->obj.rolling_ball.vel);
            
            // Check if the speed is greater than PHYLIB_VEL_EPSILON
            if (speed_a > PHYLIB_VEL_EPSILON) {
                // Set the acceleration of the ball to the negative velocity divided by the speed multiplied by PHYLIB_DRAG
                (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.vel.x / speed_a * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.vel.y / speed_a * PHYLIB_DRAG;
            }
            else{
                (*a)->obj.rolling_ball.acc.x = 0.0;
                (*a)->obj.rolling_ball.acc.y = 0.0;
            }

            if (speed_b > PHYLIB_VEL_EPSILON) {
                // Set the acceleration of the ball b to the negative velocity divided by the speed multiplied by PHYLIB_DRAG
                (*b)->obj.rolling_ball.acc.x = -(*b)->obj.rolling_ball.vel.x / speed_b * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -(*b)->obj.rolling_ball.vel.y / speed_b * PHYLIB_DRAG;
            }
            else{
                (*b)->obj.rolling_ball.acc.x = 0.0;
                (*b)->obj.rolling_ball.acc.y = 0.0;
            }

            break;
    }
}

unsigned char phylib_rolling( phylib_table *t ){
    if (t == NULL){
        return 0;
    }
    //Return num of rolling balls
    unsigned char numRolling = 0;
    
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i ++){
        if (t->object[i]!=NULL){
            if (t->object[i]->type == PHYLIB_ROLLING_BALL){
                numRolling++;
            }
        }
    }
    return numRolling;
}

phylib_table *phylib_segment(phylib_table *table) {

    int segEnd = 0;
    

    if (phylib_rolling(table) == 0) {

        return NULL;
    }

    // Create a copy of the input table
    phylib_table *new_table = phylib_copy_table(table);

    double time = PHYLIB_SIM_RATE;

    while (time < PHYLIB_MAX_TIME)
    {      
        
        // Loop to apply phylib_roll to each ROLLING_BALL
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (new_table->object[i] != NULL && new_table->object[i]->type == PHYLIB_ROLLING_BALL) {

                //Apply Roll with each incremented time
                phylib_roll(new_table->object[i], table->object[i], time);
            }
        }

        // For loop to check for collisions
        for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++)
        {
            if (new_table->object[i] == NULL)
                continue;

            if (phylib_stopped(new_table->object[i]) == 1) 
            {
                //new_table->time += time;
                segEnd = 1;
            }
            
            for (int j=0; j < PHYLIB_MAX_OBJECTS; j++)
            {
                //In case the object gets freed after entering a hole
                if (new_table->object[i] == NULL)
                    continue;
                if (new_table->object[j] == NULL)
                    continue;
                if (j == i)
                    continue;
                if (new_table->object[i] != NULL && new_table->object[i]->type != PHYLIB_ROLLING_BALL)
                    continue;
                if ((new_table->object[j] != NULL && new_table->object[j]->type == PHYLIB_ROLLING_BALL) && (j < i))
                    continue;

                //Compute distance between objects
                double dist = 0.0;
                dist = phylib_distance(new_table->object[i], new_table->object[j]);

                //Check for collision
                if (dist < 0.0 && dist != -1.0)
                {   
                    //Call bounce on colliding objects
                    phylib_bounce( &new_table->object[i], &new_table->object[j]);
                    
                    segEnd = 1;
                }

            }
        }
        //Check end flag
        if(segEnd == 1 ){

            //return
            new_table->time += time;
            return new_table;
        }
        time += PHYLIB_SIM_RATE;
    }

    return new_table;
}

//New function
char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        snprintf( string, 80, "NULL;" );
        return string;
    }
    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
            snprintf( string, 80,
                    "STILL_BALL (%d,%6.1lf,%6.1lf)",
                    object->obj.still_ball.number,
                    object->obj.still_ball.pos.x,
                    object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            snprintf( string, 80,
                    "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                    object->obj.rolling_ball.number,
                    object->obj.rolling_ball.pos.x,
                    object->obj.rolling_ball.pos.y,
                    object->obj.rolling_ball.vel.x,
                    object->obj.rolling_ball.vel.y,
                    object->obj.rolling_ball.acc.x,
                    object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            snprintf( string, 80,
                    "HOLE (%6.1lf,%6.1lf)",
                    object->obj.hole.pos.x,
                    object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            snprintf( string, 80,
                    "HCUSHION (%6.1lf)",
                    object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            snprintf( string, 80,
                "VCUSHION (%6.1lf)",
                object->obj.vcushion.x );
            break;
    }
    return string;
}
