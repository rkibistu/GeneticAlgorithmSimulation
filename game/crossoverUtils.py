import random

import evolutionSettings as settings
from entity import Entity

# gets 2 parents and returns 2 new organisms
# new organisms are made using simple weight multiplayer
def crossover(parent_1, parent_2):  
    crossover_weight = random.random()
    velocity_new1 = (crossover_weight * parent_1.v) + ((1 - crossover_weight) * parent_2.v)
    velocity_new2 = (crossover_weight * parent_2.v) + ((1 - crossover_weight) * parent_1.v)
    
    sense_new1 = (crossover_weight * parent_2.d_food_max) + ((1 - crossover_weight) * parent_1.d_food_max)
    sense_new2 = (crossover_weight * parent_1.d_food_max) + ((1 - crossover_weight) * parent_2.d_food_max)

    org_1 = Entity(settings=settings.settings,wih=parent_1.wih,who=parent_1.who,velocity=velocity_new1,sense=sense_new1)
    org_2 = Entity(settings=settings.settings,wih=parent_1.wih,who=parent_1.who,velocity=velocity_new2,sense=sense_new2)

    return org_1, org_2

# get 2 parents and returns 2 new organism
# use bits crossover: it concatanes all trait as bit strings,
# split them in k bit substrings, crossover them and reclacualte the trait
def crossover_binary(parent_1, parent_2, k):
    
    #gen bianry representation of traits to be changed
    binary_vel_1 = bin(int(parent_1.v))[2:]
    binary_vel_2 = bin(int(parent_2.v))[2:]
    binary_sense_1 = bin(int(parent_1.d_food_max))[2:]
    binary_sense_2 = bin(int(parent_2.d_food_max))[2:]

    # gen binary stirng for each paarent
    concatenated1 = binary_vel_1 + binary_sense_1 
    concatenated2 = binary_vel_2 + binary_sense_2
    
    #k is the number of lines that spltis the bit string
    # we calcualte the length of a split
    segmentLen1 = int(len(concatenated1) / k)
    segmentLen2 = int(len(concatenated2) / k)
    segmentLen = min(segmentLen1,segmentLen2)
    
    # calculate new binary strings (crossover segments)
    modified1 = ""
    modified2 = ""
    for i in range(0,k):
        if(i%2==0):
            modified1+=concatenated1[i*segmentLen:i*segmentLen+segmentLen]
            modified2+=concatenated2[i*segmentLen:i*segmentLen+segmentLen]
        else:
            modified1+=concatenated2[i*segmentLen:i*segmentLen+segmentLen]
            modified2+=concatenated1[i*segmentLen:i*segmentLen+segmentLen]
    if((k)%2==0):
        modified1+=concatenated1[k*segmentLen:]
        modified2+=concatenated2[k*segmentLen:]
    else:
        modified1+=concatenated2[k*segmentLen:]
        modified2+=concatenated1[k*segmentLen:]
    
    # modified1 now have length equal with concatenated2
    # and modified2 equal with concatenated1
    new_vel_1_binary = modified1[:len(binary_vel_2)]
    new_sense_1_binary = modified1[len(binary_vel_2):]
    
    new_vel_2_binary = modified2[:len(binary_vel_1)]
    new_sense_2_binary = modified2[len(binary_vel_1):]

    new_vel_1 = int(new_vel_1_binary,2)
    new_sense_1 = int(new_sense_1_binary,2)
    
    new_vel_2 = int(new_vel_2_binary,2)
    new_sense_2 = int(new_sense_2_binary,2)
    
    # Uncomment this to see hwo crossover affects the values of traits 
    #print("----")
    #print("1: oldV: ",parent_1.v, " newV: ",new_vel_1, " oldS: ",parent_1.d_food_max, " newS: ", new_sense_1)
    #print("2: oldV: ",parent_2.v, " newV: ",new_vel_2, " oldS: ",parent_2.d_food_max, " newS: ", new_sense_2)
    #print("----")
    
    org_1 = Entity(settings=settings.settings,wih=parent_1.wih,who=parent_1.who,velocity=new_vel_1,sense=new_sense_1)
    org_2 = Entity(settings=settings.settings,wih=parent_1.wih,who=parent_1.who,velocity=new_vel_2,sense=new_sense_2)

    return org_1, org_2
    
    
def concatenate_replace_and_split(num1, num2, x, replacement):
    # Convert numbers to binary strings
    binary1 = bin(num1)[2:]
    binary2 = bin(num2)[2:]

    # Concatenate binary strings
    concatenated = binary1 + binary2
    print(binary1)
    print(binary2)
    print(concatenated)

    # Replace first x bits with replacement
    modified = replacement + concatenated[x:]

    # Split modified bits into two parts
    split_index = len(binary1)
    modified_part1 = modified[:split_index]
    modified_part2 = modified[split_index:]

    print(modified_part1)
    print(modified_part2)

    # Convert modified binary strings back to integers
    new_num1 = int(modified_part1, 2)
    new_num2 = int(modified_part2, 2)

    return new_num1, new_num2