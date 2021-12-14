from django.shortcuts import render
from django.http import JsonResponse
# from .models import Post
import os





def create_post2(request):
    # posts = Post.objects.all()

    dir_path = os.getcwd() +'/homeworkpost_compile_grade/'
    # posts = Post.objects.all()
    response_data = {}


    if request.POST.get('action') == 'post':

        grade = request.POST.get('grade')
        lang = request.POST.get('lang')
        code = request.POST.get('code')

        def run_code(file_name) : 
            text_file = open(dir_path+file_name, "wt")
            text_file.write(code) #Providing successful values ??in dictionary type
            text_file.close()
            extension = file_name.split('.')[-1]
            print(extension)
             
            if(extension =='c') :
                print(dir_path+file_name)
                os.system('gcc -o' + dir_path + 'output_c ' + dir_path+file_name + ' && ' + dir_path + 'output_c > ' + dir_path +'output_c.txt' ) # gcc -o ouputfilename, sourcefilename
                return(dir_path+'output_c.txt')

            elif(extension =='py') :
                os.system('python ' + dir_path +file_name+' > '+dir_path + '/output_py.txt') # > write or overwrite , >> append
                return(dir_path+'output_py.txt')



        print("grade는?? : " + str(grade))
        if(grade =='1') :
            print("grade 1 진입")
            answer_list = os.listdir(dir_path + 'answer/pyramid/real_answer')
            #10개의 답에 대해서 점수를 체크한다. 
            answer_list = answer_list[1:]
            print(answer_list)
            correct =[] # 맞은 여부를 저장하는 배열
            testcase = [] #테스트 케이스를 입력하는 배열.
            answer_output_list = [] #정답의 output 내용을 저장하는 배열 
            my_answer_output_list = [] #내 코드로 결과를 낸 output 내용을 저장하는 배열
            
            #내 답안과 실제 답안 check
            for answer_file in answer_list: 
                new_code = code + '\npyramid(' + str(answer_file[0])+')' #컴파일 해야할 코드
                testcase.append(answer_file[0])
                #new_code를 .py로 저장하기
                text_file = open(dir_path + 'answer/pyramid/my_answer/'+str(answer_file[0]) +'.py', "wt")
                text_file.write(new_code) #Providing successful values ??in dictionary type
                text_file.close()
                #.py를 컴파일하기
                os.system('python ' + dir_path + 'answer/pyramid/my_answer/'+str(answer_file[0]) +'.py'+' > '+dir_path + 'answer/pyramid/my_answer/'+str(answer_file[0]) + '.txt') # > write or overwrite , >> append
                #내 답 읽어오기
                f = open(dir_path + 'answer/pyramid/my_answer/'+str(answer_file))
                my_answer = f.read()
                #실제 정답 읽어오기
                f = open(dir_path + 'answer/pyramid/real_answer/'+ str(answer_file) )
                answer = f.read()
                print("============================")
                print(answer)
                answer_output_list.append(answer)
                print(my_answer)
                my_answer_output_list.append(my_answer)
                if(answer == my_answer) : 
                    correct.append("정답")
                    response_data['isthisallcorrected'] = 1
                    print("정답을 맞췄습니다.")
                else : 
                    correct.append("오답")
                    response_data['isthisallcorrected'] = 0


            response_data['correct'] = correct
            response_data['my_answer_output_list'] = my_answer_output_list
            response_data['answer_output_list'] = answer_output_list


        else : 
            print()
            outputfile = ''
            if(lang =="C"):
                file_name = "test.c"
                outputfile = run_code(file_name)
            elif(lang == "PYTHON") :
                file_name = "test.py"
                outputfile = run_code(file_name)

            print(dir_path + "output.txt")
            f = open(outputfile, "r")
            file_content = f.read()
            f.close()
            print(file_content)

            response_data['lang'] = lang
            response_data['code'] = code
            response_data['result'] = file_content
        

        return JsonResponse(response_data)

    # return render(request, 'create_post2.html', {'posts':posts})    
    return render(request, 'homeworkpost_compile_grade/create_post2.html')   