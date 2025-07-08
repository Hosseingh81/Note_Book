from django.test import TestCase
#here you should wirte your Modelname instead of Modelname that you see here.

from django.test import TestCase
#here you should wirte your Modelname instead of Modelname that you see here.

class field_object_created_sucssefuly(TestCase): 
    def __init__(self, Model_name , Model_objects=None, methodName = "subTest"):
        self.Model_name=Model_name
        self.Model_objects=Model_objects
        super().__init__(methodName)
    

    def test_Model_object_creadted_sucssefuly(self,**field_values): #this func test that your Model object has been created sucssefuly or not.
        return self.assertIsNotNone(self.Model_name.objects.all())
    
    def test_Model_object_data_saved_correctly(self,**field_values): #this func tests that your model object data is correct, it means that data you created is the same data that saved in the database.
        if len(field_values) !=0:
            for key in field_values.keys():
                for object in self.Model_name.objects.all():
                    return self.assertEqual(field_values[key],getattr(object, key))
        else:
            try:
                return self.assertNotEqual(len(field_values),0)
            except:
                raise( AssertionError( "field_values dictionary is empty.(it doesn't have any key or value.)" ) )
            

